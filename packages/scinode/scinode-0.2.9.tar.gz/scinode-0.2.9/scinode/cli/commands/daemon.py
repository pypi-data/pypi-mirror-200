import click
from pathlib import Path
from colorama import Fore, Style


def daemon_not_exist(name, computer):
    return (
        Fore.RED
        + "Error!!! Daemon {}@{} is not setup.\n".format(name, computer)
        + Style.RESET_ALL
    )


def start_daemon(
    ctx, name, data, pool=None, concurrency=None, sleep=None, foreground=None
):
    print(f"Start daemon: {name}")
    if ctx.obj.use_celery:
        from scinode.engine.celery.daemon import CeleryDaemon

        kwargs = {}
        if data["broker"]:
            concurrency = 1
            kwargs["queue"] = "broker"
        else:
            kwargs["queue"] = name
        if concurrency:
            kwargs["concurrency"] = concurrency
        if pool:
            kwargs["pool"] = pool
        daemon = CeleryDaemon(name=name, **kwargs)
        daemon.start()
    else:
        from scinode.daemon.daemon import ScinodeDaemon

        daemon = ScinodeDaemon(name, pool=pool, concurrency=concurrency, sleep=sleep)
        print("Start daemon {}, sleep: {}".format(daemon.name, sleep))
        if foreground:
            daemon.run()
        else:
            daemon.start()


@click.group(help="CLI tool to manage Daemon.")
def daemon():
    pass


@daemon.command(help="Start the daemon.")
@click.argument("name", default="broker", type=str)
@click.option(
    "-p",
    "--pool",
    type=click.Choice(
        ["prefork", "thread", "process", "gevent", "eventlet"], case_sensitive=False
    ),
    default="prefork",
)
@click.option("-c", "--concurrency", help="concurrency", type=int)
@click.option("--foreground", is_flag=True, default=False, help="Use foreground mode")
@click.option("-s", "--sleep", default=1, help="Sleep time")
@click.pass_context
def start(ctx, name, pool, concurrency, foreground, sleep):
    """Start worker instance.

    Examples
    --------

    scinode daemon start localhost --concurrency=100 --pool eventlet
    """
    from scinode.database.client import scinodedb
    from scinode.database.daemon import DaemonClient

    computer = ctx.obj.activate_profile["computer"]
    data = scinodedb["daemon"].find_one({"name": name, "computer": computer})
    if data is None:
        print(daemon_not_exist(name, computer))
        print("Please setup a new one or choose daemon from:")
        client = DaemonClient()
        client.show({"computer": computer})
        return
    start_daemon(
        ctx,
        name,
        data,
        pool=pool,
        concurrency=concurrency,
        foreground=foreground,
        sleep=sleep,
    )


@daemon.command(help="Stop the daemon.")
@click.argument("name", default="broker", type=str)
@click.option("--computer", help="Computer", type=str)
@click.pass_context
def stop(ctx, name, computer=None):
    from scinode.database.daemon import DaemonClient

    daemon_client = DaemonClient()
    if not computer:
        computer = ctx.obj.activate_profile["computer"]
    data = daemon_client.get_daemon(name, computer)
    if data is None:
        print(daemon_not_exist(name, computer))
    if ctx.obj.use_celery:
        ctx.obj.app.control.broadcast("shutdown", destination=[f"{name}@{computer}"])
    else:
        from scinode.utils.db import push_message

        push_message(name, f"{name},daemon,STOP")


@daemon.command(help="Stop all daemon.")
@click.pass_context
def stop_all(ctx):
    if ctx.obj.use_celery:
        ctx.obj.app.control.broadcast("shutdown")
    else:
        from scinode.utils.db import push_message
        from scinode.database.daemon import DaemonClient

        daemon = DaemonClient()
        data = daemon.get_data()
        for d in data:
            push_message(d["name"], f"{d['name']},daemon,STOP")


@daemon.command(help="Restart the daemon.")
@click.argument("name", default="broker", type=str)
@click.option("--computer", help="Computer", type=str)
@click.pass_context
def restart(ctx, name, computer=None):
    from scinode.database.daemon import DaemonClient

    daemon_client = DaemonClient()
    if not computer:
        computer = ctx.obj.activate_profile["computer"]
    data = daemon_client.get_daemon(name, computer)
    if data is None:
        print(daemon_not_exist(name, computer))
    if ctx.obj.use_celery:
        ctx.obj.app.control.broadcast(
            "pool_restart", destination=[f"{name}@{computer}"]
        )
    else:
        from scinode.utils.db import push_message

        push_message(name, f"{name},daemon,RESTART")


@daemon.command(help="Restart the daemon.")
@click.argument("name", default="broker", type=str)
@click.option(
    "--pool",
    type=click.Choice(["thread", "process", "celery"], case_sensitive=False),
    default="thread",
)
@click.option("--concurrency", default=0, help="Sleep time")
@click.option("--sleep", default=1, help="Sleep time")
def hard_restart(name, pool, concurrency, sleep):
    from scinode.daemon.daemon import ScinodeDaemon

    daemon = ScinodeDaemon(name, pool=pool, concurrency=concurrency, sleep=sleep)
    daemon.restart()


@daemon.command(help="Show the log file of the daemon.")
@click.option("--limit", help="Number of lines to be shown.", default=100, type=int)
@click.argument("name", default="broker", type=str)
def log(name, limit):
    from scinode.daemon.daemon import ScinodeDaemon

    daemon = ScinodeDaemon(name=name)
    daemon.showlog(limit)


@daemon.command(help="Add new daemon.")
@click.option("--file", help="Read configuration from file.", type=str)
@click.pass_context
def add(ctx, file):
    from scinode.daemon.config import DaemonConfig

    if file:
        DaemonConfig.add_from_json(file)
    else:
        name = click.prompt("Name of this daemon:", default="broker")
        default_path = str(Path.home() / "scinode")
        broker = click.prompt("Is this a broker daemon:", default="Yes", type=bool)
        workdir = click.prompt("Default working directory:", default=default_path)
        if ctx.obj.use_celery:
            config = DaemonConfig(name=name, workdir=workdir, broker=broker)
            config.save_to_db()
        else:
            sleep = click.prompt("Sleep time:", default=1, type=float)
            config = DaemonConfig(
                name=name, workdir=workdir, sleep=sleep, broker=broker
            )
            config.save_to_db()


@daemon.command(help="Delete daemons.")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete the daemons?")
def delete(name):
    from scinode.daemon.daemon import ScinodeDaemon
    from scinode.database.client import scinodedb
    from scinode.database.daemon import DaemonClient
    import datetime

    client = DaemonClient()
    query = {"name": name}
    datas = scinodedb["daemon"].find_one(query, {"_id": 0})
    daemon = ScinodeDaemon(name=datas["name"])
    d = daemon.data
    t = int((datetime.datetime.utcnow() - d["lastUpdate"]).total_seconds())
    if t < 2 * d["sleep"]:
        print(
            "Daemon {} is likely running now. Please stop it first.".format(
                datas["name"]
            )
        )
    else:
        print("Delete daemon: {}".format(datas["name"]))
        client.delete("daemon", {"uuid": datas["uuid"]})


@daemon.command(help="List daemons.")
@click.option("--name", help="Name of the item.")
@click.option("--index", help="Index of the item.", type=int)
@click.option("--uuid", help="uuid of the item.")
@click.option("--state", help="state of the item.")
def list(name, index, uuid, state):
    from scinode.database.daemon import DaemonClient

    client = DaemonClient()
    query = {}
    if name:
        query["name"] = name
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    client.list(query)


@daemon.command(help="Show the data of a daemon.")
@click.argument("name", default="broker", type=str)
def show(name):
    from scinode.database.daemon import DaemonClient

    client = DaemonClient()
    query = {}
    query["name"] = name
    client.show(query)


@daemon.command(help="Show the status of a daemon.")
@click.option("--name", help="Name of the item.")
@click.pass_context
def status(ctx, name):
    from scinode.database.daemon import DaemonClient

    daemon_client = DaemonClient()
    query = {}
    data = daemon_client.get_data()
    if ctx.obj.use_celery:
        reply = ctx.obj.app.control.inspect()
        active = reply.active()
        # print(active)
        for d in data:
            daemon_name = f"{d['name']}@{d['computer']}"
            if active is not None and daemon_name in active:
                d["running"] = True
                print(
                    "{:20s}:   {}".format(
                        daemon_name, Fore.GREEN + "Running" + Style.RESET_ALL
                    )
                )
            else:
                print(
                    "{:20s}:   {}".format(
                        daemon_name, Fore.RED + "Stop" + Style.RESET_ALL
                    )
                )
    else:
        if name:
            query["name"] = name
        daemon_client.status(query)

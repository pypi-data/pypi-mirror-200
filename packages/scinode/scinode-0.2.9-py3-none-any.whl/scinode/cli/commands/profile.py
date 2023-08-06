import click


@click.group(help="CLI tool to manage profiles.")
def profile():
    pass


@profile.command(help="Reset profile.")
@click.confirmation_option(
    prompt="This will delete all data in the database for this profile. Are you reset?"
)
def reset():
    from scinode.database.db import ScinodeDB

    db = ScinodeDB()
    for name in ["nodetree", "node", "daemon", "broker"]:
        db.reset(name)


@profile.command(help="Delete profile.")
@click.argument("name")
@click.confirmation_option(
    prompt="This will delete all data for the profile. Are you delete?"
)
def delete(name):
    from scinode.profile import ScinodeProfile

    p = ScinodeProfile()
    p.delete(query={"name": name})


@profile.command(help="Add profile")
@click.option("--file", help="Add profile from file.", type=str)
def add(file):
    import socket
    from scinode.profile import ScinodeProfile
    from pathlib import Path

    p = ScinodeProfile()
    if file:
        import json

        with open(file, "r") as f:
            datas = json.load(f)
            datas["activate"] = False
            p.insert_one(datas)
    else:
        name = click.prompt("Name of the profile:", default="scinode")
        computer = click.prompt("Name of the computer:", default=socket.gethostname())
        db_address = click.prompt(
            "Address of mongodb service:", default="mongodb://localhost:27017/"
        )
        db_name = click.prompt("Name of the database:", default="scinode_db")
        default_config_path = str(Path.home() / ".scinode")
        config_path = click.prompt(
            "Default configuration directory:", default=default_config_path
        )
        celery = click.prompt("Use celery:", default="Yes", type=bool)
        if celery:
            broker_url = click.prompt(
                "Address of rabbitmq service:", default="amqp://localhost//"
            )
        else:
            broker_url = "amqp://localhost//"
        datas = {
            "name": name,
            "computer": computer,
            "db_address": db_address,
            "db_name": db_name,
            "config_path": config_path,
            "celery": celery,
            "broker_url": broker_url,
            "activate": False,
        }
        p.insert_one(datas)


@profile.command(help="Show profile")
@click.argument("name", default="", type=str)
@click.pass_context
def show(ctx, name):
    ctx.obj.profile.show(name)


@profile.command(help="list profile")
def list():
    from scinode.profile import ScinodeProfile

    p = ScinodeProfile()
    p.list()


@profile.command(help="use profile")
@click.argument("name")
def use(name):
    from scinode.profile import ScinodeProfile

    p = ScinodeProfile()
    p.use(name)

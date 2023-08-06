import click


@click.group(help="CLI tool to manage message queue.")
def mq():
    pass


@mq.command(help="Show the log file of the message queue.")
@click.option("--limit", help="Number of lines to be shown.", default=100, type=int)
@click.argument("name", default="broker", type=str)
def log(name, limit):
    from scinode.engine.mq import MQ

    mq = MQ(name=name)
    mq.show(limit=limit)


@mq.command(help="clean the message queue.")
@click.argument("name", default="broker", type=str)
def clean(name):
    """Clean mq."""
    from scinode.database.db import scinodedb

    scinodedb["mq"].update_one({"name": name}, {"$set": {"msg": [], "indices": [0]}})

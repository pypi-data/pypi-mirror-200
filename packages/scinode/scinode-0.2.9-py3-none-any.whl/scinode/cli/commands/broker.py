import click
from pathlib import Path
import os


@click.group(help="CLI tool to manage broker.")
def broker():
    pass


@broker.command(help="Show the log file of the broker.")
@click.option("--limit", help="Number of lines to be shown.", default=100, type=int)
@click.argument("name", default="localhost", type=str)
def log(name, limit):
    from scinode.engine.mq import Broker

    broker = Broker(name=name)
    broker.show()


@broker.command(help="clean the broker.")
@click.argument("name", default="localhost", type=str)
def clean(name):
    """Clean broker."""
    from scinode.database.db import scinodedb

    scinodedb["broker"].update_one(
        {"name": name}, {"$set": {"msg": [], "indices": [0]}}
    )

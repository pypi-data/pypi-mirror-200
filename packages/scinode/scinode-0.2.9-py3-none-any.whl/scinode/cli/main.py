#!/usr/bin/env python
import pkg_resources
import click
from scinode.profile import ScinodeProfile


class CLIContext:
    """Context Object for the CLI."""

    def __init__(self, app=None):
        """Initialize the CLI context."""
        self.profile = ScinodeProfile()
        self.activate_profile = self.profile.load_activate_profile()
        self.app = app
        if self.activate_profile is not None and self.activate_profile["celery"]:
            from scinode.engine.celery.tasks import app

            self.app = app
            self.use_celery = True
        else:
            self.use_celery = False


@click.group(help="CLI tool to manage SciNode")
@click.pass_context
def scinode(ctx):
    ctx.obj = CLIContext()


def load_entry_point():
    for entry_point in pkg_resources.iter_entry_points("scinode_cli"):
        scinode.add_command(entry_point.load())


load_entry_point()

if __name__ == "__main__":
    scinode()

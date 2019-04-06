import os
from time import sleep

import click

from idact.core.nodes import Nodes

SLEEP_INTERVAL = 10


def sleep_until_allocation_ends(nodes: Nodes):
    """Sleeps until the allocation ends."""
    while nodes.running():
        click.echo("Nodes are still running.")
        sleep(SLEEP_INTERVAL)

        if 'IDACT_TEST_NOTEBOOK_APP_TEST_RUN' in os.environ:
            click.echo("This is a test run, cancelling the allocation.")
            nodes.cancel()

    click.echo(click.style("Nodes are no longer running.", fg='red'))

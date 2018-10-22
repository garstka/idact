from time import sleep

import click

from idact.core.nodes import Nodes

SLEEP_INTERVAL = 10


def sleep_until_allocation_ends(nodes: Nodes):
    """Sleeps until the allocation ends."""
    while nodes.running():
        click.echo("Nodes are still running.")
        sleep(SLEEP_INTERVAL)
    click.echo(click.style("Nodes are no longer running.", fg='red'))

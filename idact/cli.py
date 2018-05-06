# -*- coding: utf-8 -*-

"""Console script for idact."""
import sys
import click


@click.command()
def main():
    """Console script for idact."""
    click.echo("Test")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

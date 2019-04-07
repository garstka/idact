from pprint import pprint

from idact import Node


def check_no_output(node: Node, command: str):
    """Check the command produces no output."""
    output = node.run(command).splitlines()
    pprint(output)
    assert not output

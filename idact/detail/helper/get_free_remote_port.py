from idact.core.nodes import Node


def get_free_remote_port(node: Node) -> int:
    """Returns a free remote port.

        :param node: Node to find a port on.

    """
    output = node.run("python -c 'import socket; s=socket.socket();"
                      " s.bind((str(), 0)); print(s.getsockname()[1]);"
                      " s.close()'")
    return int(output)

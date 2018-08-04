from idact.core.nodes import Node


def get_free_remote_port(node: Node) -> int:
    """Returns a free remote port.

        Uses a Python snippet to determine a free port by binding a socket
        to port 0 and immediately releasing it.

        :param node: Node to find a port on.

    """
    output = node.run("python -c 'import socket; s=socket.socket();"
                      " s.bind((str(), 0)); print(s.getsockname()[1]);"
                      " s.close()'")
    return int(output)

import socket


def get_free_local_port() -> int:
    """Returns a free local port.

        Binds a socket to port 0 and immediately releases it.

    """
    with socket.socket() as sock:
        sock.bind(("", 0))
        return sock.getsockname()[1]

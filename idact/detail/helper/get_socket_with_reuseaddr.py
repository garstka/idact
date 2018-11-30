import socket


def get_socket_with_reuseaddr() -> socket.socket:
    """Returns a new socket with `SO_REUSEADDR` option on, so an address
        can be reused immediately, without waiting for TIME_WAIT socket
        state to finish.

        On Windows, `SO_EXCLUSIVEADDRUSE` is used instead.
        This is because `SO_REUSEADDR` on this platform allows the socket
        to be bound to an address that is already bound by another socket,
        without requiring the other socket to have this option on as well.

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if 'SO_EXCLUSIVEADDRUSE' in dir(socket):
        sock.setsockopt(socket.SOL_SOCKET,
                        getattr(socket, 'SO_EXCLUSIVEADDRUSE'), 1)
    else:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    return sock

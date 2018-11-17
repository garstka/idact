from idact.detail.log.get_logger import get_logger
from idact.detail.helper.get_socket_with_reuseaddr import \
    get_socket_with_reuseaddr

LOCAL_BIND_ADDRESS = ""


def is_local_port_taken(port: int) -> bool:
    """Returns True if local port is taken (unable to bind to it).

        :param port: Port to check.

    """
    with get_socket_with_reuseaddr() as sock:
        try:
            sock.bind((LOCAL_BIND_ADDRESS, port))
        except Exception:  # noqa, pylint: disable=broad-except
            log = get_logger(__name__)
            log.debug("Exception, port probably taken.", exc_info=1)
            return True

    return False

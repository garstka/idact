from threading import Thread
from time import sleep

from tests.helpers.paramiko_connect import paramiko_connect
from tests.helpers.test_users import USER_4


def run_dummy_server(server_port: int, timeout: float):
    """Runs a simple HTTP server on the testing container.

        :param server_port: Remote server port.

        :param timeout: Timeout in seconds.
    """
    with paramiko_connect(user=USER_4) as ssh:
        ssh.exec_command(
            "python3 -m http.server {server_port}".format(
                server_port=server_port))
        sleep(timeout)
        ssh.exec_command("killall python3")


STARTUP_TIME = 1


def start_dummy_server_thread(server_port: int, timeout: float = 5) -> Thread:
    """Runs a simple HTTP server in a separate thread.w
       See :func:`run_dummy_server`."""

    server = Thread(target=run_dummy_server, args=(server_port, timeout))
    server.start()
    sleep(STARTUP_TIME)
    return server

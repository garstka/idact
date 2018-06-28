from threading import Thread
from time import sleep

import paramiko

from tests.helpers.reset_environment import get_testing_host, get_testing_port
from tests.helpers.test_users import USER_4, get_test_user_password


def run_dummy_server(server_port: int, timeout: float):
    """Runs a simple HTTP server on the testing container.

        :param server_port: Remote server port.

        :param timeout: Timeout in seconds.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(hostname=get_testing_host(),
                port=get_testing_port(),
                username=USER_4,
                password=get_test_user_password(USER_4),
                look_for_keys=False)
    ssh.exec_command(
        "python3 -m http.server {server_port}".format(
            server_port=server_port))
    sleep(timeout)
    ssh.exec_command("killall python3")


STARTUP_TIME = 2


def start_dummy_server_thread(server_port: int, timeout: float = 3) -> Thread:
    """Runs a simple HTTP server in a separate thread.w
       See :func:`run_dummy_server`."""

    server = Thread(target=run_dummy_server, args=(server_port, timeout))
    server.start()
    sleep(STARTUP_TIME)
    return server

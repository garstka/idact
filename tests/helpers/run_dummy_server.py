from threading import Thread
from time import sleep

from tests.helpers.paramiko_connect import paramiko_connect


def run_dummy_server(user: str,
                     server_port: int,
                     timeout: float):
    """Runs a simple HTTP server on the testing container as the given user.

        :param user: User to run the server as.

        :param server_port: Remote server port.

        :param timeout: Time to run the server for in seconds.

    """
    with paramiko_connect(user=user) as ssh:
        try:
            ssh.exec_command(
                "python -m SimpleHTTPServer {server_port}".format(
                    server_port=server_port))
            sleep(timeout)
        finally:
            ssh.exec_command("kill"
                             " `ps -U $USER"
                             " | grep python"
                             " | awk '{ print $1 }'`")


STARTUP_TIME = 1


def start_dummy_server_thread(user: str,
                              server_port: int,
                              timeout: float = 5) -> Thread:
    """Runs a simple HTTP server on the cluster by starting it and stopping
        after a while, in a separate thread.

        See :func:`run_dummy_server`.

        :param user: User to run the server as.

        :param server_port: Remote server port.

        :param timeout: Time to run the server for in seconds.

    """

    server = Thread(target=run_dummy_server, args=(user, server_port, timeout))
    server.start()
    sleep(STARTUP_TIME)
    return server

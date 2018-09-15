from contextlib import contextmanager

from tests.helpers.paramiko_connect import paramiko_connect


@contextmanager
def remove_remote_file(user: str, path: str):
    """A context manager that removes a remote file on exit.

        :param user: User to connect as.

        :param path: Remote file path to remove.

    """
    try:
        yield
    finally:
        with paramiko_connect(user=user) as ssh:
            ssh.exec_command(command="rm -f {path} || exit 0".format(
                path=path))

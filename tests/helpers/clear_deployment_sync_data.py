from contextlib import contextmanager

from idact.detail.deployment_sync.deployment_definitions_serialization import \
    DEPLOYMENT_DEFINITIONS_PATH, DEPLOYMENT_DEFINITIONS_FILENAME
from tests.helpers.paramiko_connect import paramiko_connect


@contextmanager
def clear_deployment_sync_data(user: str):
    """Clears the deployment sync data from user directory.

        :param user: User, whose home directory should be cleared.

    """
    try:
        yield
    finally:
        with paramiko_connect(user=user) as ssh:
            ssh.exec_command(command="rm -f {}/{}".format(
                DEPLOYMENT_DEFINITIONS_PATH,
                DEPLOYMENT_DEFINITIONS_FILENAME))

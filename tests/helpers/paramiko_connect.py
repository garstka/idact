import paramiko

from tests.helpers.test_users import get_test_user_password
from tests.helpers.testing_environment \
    import get_testing_host, get_testing_port


class IgnorePolicy(paramiko.MissingHostKeyPolicy):
    """Ignore missing host key."""

    def missing_host_key(self, client, hostname, key):
        pass


def paramiko_connect(user: str) -> paramiko.SSHClient:
    """Connects to cluster using low-level SSH client."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(IgnorePolicy())
    ssh.connect(hostname=get_testing_host(),
                port=get_testing_port(),
                username=user,
                password=get_test_user_password(user),
                look_for_keys=False)
    return ssh

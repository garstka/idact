import os

TEST_CLUSTER = 'test'
"""Test cluster name."""

TEST_KEY_LOCATION = os.path.join(os.getcwd(), '.test-ssh-{user}')
"""Location for generated SSH keys. By default, this would be `~/.ssh`."""

TEST_ENVIRONMENT_FILE = './idact.test.conf-{user}'
"""Environment file for tests."""

SLURM_WAIT_TIMEOUT = 360
"""Timeout for test allocations."""


def get_testing_host() -> str:
    """Returns the testing setup hostname, currently hard-coded to `localhost`.
    """
    return 'localhost'


def get_testing_port() -> int:
    """Returns the port for connection to the testing setup host.
        The port is determined by the environment variable
        :attr:`IDACT_TEST_CONTAINER_SSH_PORT`,
        or defaults to 2222 if it's missing.
    """
    return int(os.environ.get('IDACT_TEST_CONTAINER_SSH_PORT', 2222))


def get_test_key_location(user: str) -> str:
    """Returns the directory path for test SSH keys.

        :param user: User name.

    """
    return TEST_KEY_LOCATION.format(user=user)


def get_test_environment_file(user: str) -> str:
    """Returns the config file to save during a test if needed.

        :param user: User name.

    """
    return TEST_ENVIRONMENT_FILE.format(user=user)


def get_testing_process_count() -> int:
    """Returns the testing process count."""
    return int(os.environ.get('IDACT_TESTING_PROCESS_COUNT', 1))

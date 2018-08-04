import os

TEST_CLUSTER = 'test'
"""Test cluster name."""

TEST_KEY_LOCATION = os.path.join(os.getcwd(), '.test-ssh')
"""Location for generated SSH keys. By default, this would be `~/.ssh`."""


def get_testing_host():
    """Returns the testing setup hostname, currently hard-coded to `localhost`.
    """
    return 'localhost'


def get_testing_port():
    """Returns the port for connection to the testing setup host.
        The port is determined by the environment variable :attr:`SLURM_PORT`,
        or defaults to 2222 if it's missing.
    """
    return os.environ.get('SLURM_PORT', 2222)

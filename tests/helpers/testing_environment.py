import os

TEST_CLUSTER = 'test'
"""Test cluster name."""

TEST_KEY_LOCATION = os.path.join(os.getcwd(), '.test-ssh')
"""Location for generated SSH keys. By default, this would be '~/.ssh'."""


def get_testing_host():
    return 'localhost'


def get_testing_port():
    return os.environ.get('SLURM_PORT', 2222)

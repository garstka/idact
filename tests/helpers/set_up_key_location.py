import os
import shutil
from contextlib import contextmanager

from tests.helpers.testing_environment import get_test_key_location


@contextmanager
def set_up_key_location(user: str):
    """A context manager that sets up the target directory for generated
        SSH keys, and removes it afterwards.

        :param user: User name to be the directory name component.

        :raises AssertionError: If the directory already exists.

    """

    test_key_location = get_test_key_location(user=user)
    os.environ['IDACT_KEY_LOCATION'] = test_key_location

    assert not os.path.exists(test_key_location)
    os.mkdir(test_key_location)
    try:
        yield
    finally:
        shutil.rmtree(test_key_location)

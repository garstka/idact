import os
import shutil
from contextlib import contextmanager

from tests.helpers.reset_environment import TEST_KEY_LOCATION


@contextmanager
def set_up_key_location():
    """Sets up the target directory for generated SSH keys."""

    test_key_location = TEST_KEY_LOCATION
    os.environ['IDACT_KEY_LOCATION'] = test_key_location

    assert not os.path.exists(test_key_location)
    os.mkdir(test_key_location)
    try:
        yield
    finally:
        shutil.rmtree(test_key_location)

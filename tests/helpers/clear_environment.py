import logging
import os
from contextlib import contextmanager

from idact.core.set_log_level import set_log_level
from idact.detail.environment.environment_impl import EnvironmentImpl
from idact.detail.environment.environment_provider import EnvironmentProvider
from tests.helpers.clear_home import clear_home


@contextmanager
def clear_environment(user: str):
    """Clears the environment, but does not add any clusters.

        :param user: User, whose home dir should be cleaned.

    """
    # pylint: disable=protected-access
    saved_state = EnvironmentProvider._state
    EnvironmentProvider._state = None
    EnvironmentProvider(initial_environment=EnvironmentImpl())
    set_log_level(logging.DEBUG)
    os.environ['IDACT_CONFIG_PATH'] = './idact.test.conf'
    try:
        yield
    finally:
        EnvironmentProvider._state = saved_state
        clear_home(user=user)

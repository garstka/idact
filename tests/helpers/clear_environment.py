import logging
from contextlib import contextmanager

from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_provider import EnvironmentProvider
from tests.helpers.clear_home import clear_home


@contextmanager
def clear_environment(user: str):
    # pylint: disable=protected-access
    saved_state = EnvironmentProvider._state
    EnvironmentProvider._state = None
    EnvironmentProvider(initial_environment=Environment())
    logging.disable(logging.INFO)
    try:
        yield
    finally:
        EnvironmentProvider._state = saved_state
        clear_home(user=user)

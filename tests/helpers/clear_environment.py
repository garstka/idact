from contextlib import contextmanager

from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_provider import EnvironmentProvider

TEST_CLUSTER = 'test'


@contextmanager
def clear_environment():
    # pylint: disable=protected-access
    saved_state = EnvironmentProvider._state
    EnvironmentProvider._state = None
    EnvironmentProvider(initial_environment=Environment())
    yield
    EnvironmentProvider._state = saved_state

import os
from contextlib import contextmanager
from logging import DEBUG

from idact import AuthMethod
from idact.core.set_log_level import set_log_level
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_provider import EnvironmentProvider
from tests.helpers.clear_home import clear_home
from tests.helpers.testing_environment import TEST_KEY_LOCATION, \
    get_testing_host, get_testing_port, TEST_CLUSTER


@contextmanager
def reset_environment(user: str, auth: AuthMethod = AuthMethod.ASK):
    # pylint: disable=protected-access
    saved_state = EnvironmentProvider._state
    EnvironmentProvider._state = None

    os.environ['IDACT_KEY_LOCATION'] = TEST_KEY_LOCATION

    cluster = ClientClusterConfig(
        host=get_testing_host(),
        port=get_testing_port(),
        user=user,
        auth=auth)
    EnvironmentProvider(
        initial_environment=Environment(
            config=ClientConfig(
                clusters={TEST_CLUSTER: cluster})))
    set_log_level(DEBUG)
    try:
        yield
    finally:
        EnvironmentProvider._state = saved_state
        clear_home(user=user)

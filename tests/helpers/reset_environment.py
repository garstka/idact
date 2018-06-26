import os
from contextlib import contextmanager

from idact import AuthMethod
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_provider import EnvironmentProvider

TEST_CLUSTER = 'test'


@contextmanager
def reset_environment(user: str, auth: AuthMethod = AuthMethod.ASK):
    # pylint: disable=protected-access
    saved_state = EnvironmentProvider._state
    EnvironmentProvider._state = None

    cluster = ClientClusterConfig(
        host='localhost',
        port=os.environ.get('SLURM_PORT', 2222),
        user=user,
        auth=auth)
    EnvironmentProvider(
        initial_environment=Environment(
            config=ClientConfig(
                clusters={TEST_CLUSTER: cluster})))
    yield
    EnvironmentProvider._state = saved_state

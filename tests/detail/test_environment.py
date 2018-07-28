from idact.core.cluster import Cluster
from idact.core.auth import AuthMethod
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_provider import EnvironmentProvider


def test_create_environment():
    cluster1 = ClientClusterConfig(host='host1',
                                   port=22,
                                   user='user1',
                                   auth=AuthMethod.ASK)
    config = ClientConfig(clusters={'cluster1': cluster1})
    environment = Environment(config=config)

    assert environment.config is config
    assert len(environment.config.clusters) == 1
    assert len(environment.clusters) == 1
    assert isinstance(environment.clusters['cluster1'], Cluster)

    cluster2 = ClientClusterConfig(host='host2',
                                   port=22,
                                   user='user2',
                                   auth=AuthMethod.ASK)
    environment.add_cluster(name='cluster2', config=cluster2)

    assert len(environment.config.clusters) == 2
    assert len(environment.clusters) == 2
    assert isinstance(environment.clusters['cluster2'], Cluster)


def test_environment_provider():
    cluster1 = ClientClusterConfig(host='host1',
                                   port=22,
                                   user='user1',
                                   auth=AuthMethod.ASK)
    config = ClientConfig(clusters={'cluster1': cluster1})
    environment = Environment(config=config)

    EnvironmentProvider._state = None  # pylint: disable=protected-access
    environment_provider = EnvironmentProvider(initial_environment=environment)
    assert EnvironmentProvider._state == environment_provider.__dict__  # noqa, pylint: disable=protected-access,line-too-long
    assert environment_provider.environment is environment

    cluster2 = ClientClusterConfig(host='host2',
                                   port=22,
                                   user='user2',
                                   auth=AuthMethod.ASK)
    config2 = ClientConfig(clusters={'cluster2': cluster2})
    environment2 = Environment(config=config2)
    environment_provider2 = EnvironmentProvider(
        initial_environment=environment2)

    assert environment_provider2.environment is environment

    environment_provider2.environment = environment2
    assert environment_provider2.environment is environment2
    assert environment_provider.environment is environment2
    EnvironmentProvider._state = None  # pylint: disable=protected-access

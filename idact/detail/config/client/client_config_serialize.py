from idact.core.auth import AuthMethod
from idact.detail.config.client. \
    client_cluster_config import ClientClusterConfig
from idact.detail.config.client.client_config import ClientConfig


def serialize_client_config_to_json(config: ClientConfig) -> dict:
    """Serializes a :class:`ClientConfig` to json.

        :param config: The object to serialize."""
    return {'clusters': {name: {'host': cluster_config.host,
                                'port': cluster_config.port,
                                'user': cluster_config.user,
                                'auth': str(cluster_config.auth).split('.')[1]}
                         for name, cluster_config in config.clusters.items()}}


def deserialize_client_config_from_json(data: dict) -> ClientConfig:
    """Deserializes :class:`ClientConfig` from json.

        :param data: json to deserialize."""
    clusters = {name: ClientClusterConfig(host=value['host'],
                                          port=value['port'],
                                          user=value['user'],
                                          auth=AuthMethod[value['auth']])
                for name, value in data['clusters'].items()}
    return ClientConfig(clusters=clusters)

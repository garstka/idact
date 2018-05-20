from typing import Optional

from idact.core.auth import AuthMethod
from idact.core.cluster import Cluster
from idact.detail.config.client. \
    client_cluster_config import ClientClusterConfig
from idact.detail.environment.environment_provider import EnvironmentProvider


def add_cluster(name: str,
                user: str,
                host: str,
                port: int = 22,
                auth: Optional[AuthMethod] = None) -> Cluster:
    """Adds a new cluster.

        :param name:
            Cluster name to identify it by.
        :param user:
            Remote cluster user to log in and run commands as.
        :param host:
            Cluster access node hostname.
        :param port:
            SSH port to access the cluster.
            Default: 22.
        :param auth:
            Authentication method.
            Default: :attr:`.AuthMethod.ASK` (password-based).
       """

    environment = EnvironmentProvider().environment
    if auth is None:
        auth = AuthMethod.ASK

    client_config = ClientClusterConfig(host=host,
                                        port=port,
                                        user=user,
                                        auth=auth)
    return environment.add_cluster(name=name,
                                   client_config=client_config)

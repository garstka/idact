from typing import Optional, Dict

from idact.core.cluster import Cluster
from idact.detail.cluster_impl import ClusterImpl
from idact.detail.config.client. \
    client_cluster_config import ClientClusterConfig
from idact.detail.config.client.client_config import ClientConfig


class Environment:
    """User working environment.

        :param config: Client-side configuration. Default: empty.
    """

    def __init__(self, config: Optional[ClientConfig] = None):
        self._config = ClientConfig(clusters={}) if not config else config
        self._clusters = {name: ClusterImpl(client_config=cluster_config)
                          for name, cluster_config
                          in self._config.clusters.items()}

    @property
    def config(self) -> ClientConfig:
        """Client-side configuration."""
        return self._config

    @property
    def clusters(self) -> Dict[str, Cluster]:
        """All :class:`.Cluster` objects defined by configuration."""
        return self._clusters

    def add_cluster(self,
                    name: str,
                    client_config: ClientClusterConfig) -> Cluster:
        """Adds a cluster to config and cluster list.
           Returns the added :class:`.Cluster`.

            :param name:          Cluster name.

            :param client_config: Client-side cluster config.
        """

        self.config.add_cluster(name=name,
                                config=client_config)
        cluster = ClusterImpl(client_config=client_config)
        self.clusters[name] = cluster

        return cluster

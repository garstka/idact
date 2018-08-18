"""This module contains the implementation of an idact environment."""

from typing import Optional, Dict

from idact.core.cluster import Cluster
from idact.detail.cluster_impl import ClusterImpl
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.log.logger_provider import LoggerProvider
from idact.detail.log.set_fabric_log_level import set_fabric_log_level


class Environment:
    """User working environment.

        :param config: Client-side configuration. Default: empty.
    """

    def __init__(self, config: Optional[ClientConfig] = None):
        self._config = ClientConfig(clusters={}) if not config else config
        self._clusters = {name: ClusterImpl(config=cluster_config)
                          for name, cluster_config
                          in self._config.clusters.items()}
        self.set_log_level(level=self._config.log_level)

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
                    config: ClusterConfigImpl) -> Cluster:
        """Adds a cluster to config and cluster list.
            Returns the added :class:`.Cluster`.

             :param name:   Cluster name.

             :param config: Client-side cluster config.
        """

        self.config.add_cluster(name=name, config=config)
        cluster = ClusterImpl(config=config)
        self.clusters[name] = cluster

        return cluster

    def set_log_level(self, level: int):
        """Sets the log level for idact.

            See :func:`.set_log_level`.

            :param level: Log level.

        """
        self._config.log_level = level
        set_fabric_log_level(level=level)
        LoggerProvider().log_level = level

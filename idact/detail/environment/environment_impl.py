"""This module contains the implementation of an idact environment."""

from typing import Optional, Dict

from idact.core.cluster import Cluster
from idact.detail.cluster_impl import ClusterImpl
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment import Environment
from idact.detail.log.set_paramiko_log_level import set_paramiko_log_level


class EnvironmentImpl(Environment):
    """User working environment implementation.

        :param config: Client-side configuration. Default: empty.

    """

    def __init__(self, config: Optional[ClientConfig] = None):
        self._config = ClientConfig(clusters={}) if not config else config
        self._clusters = {name: ClusterImpl(name=name,
                                            config=cluster_config)
                          for name, cluster_config
                          in self._config.clusters.items()}
        self.set_log_level(level=self._config.log_level)

    @property
    def config(self) -> ClientConfig:
        return self._config

    @property
    def clusters(self) -> Dict[str, Cluster]:
        return self._clusters

    def add_cluster(self,
                    name: str,
                    config: ClusterConfigImpl) -> Cluster:
        self.config.add_cluster(name=name, config=config)
        cluster = ClusterImpl(name=name, config=config)
        self.clusters[name] = cluster

        return cluster

    def remove_cluster(self, name: str):
        """Removes the cluster from config and cluster list.

             :param name:   Cluster name.
        """
        try:
            self.config.remove_cluster(name=name)
        finally:
            self.clusters.pop(name)

    def set_log_level(self, level: int):
        self._config.log_level = level
        set_paramiko_log_level()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

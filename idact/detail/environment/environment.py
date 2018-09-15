"""This module contains the implementation of an idact environment."""
from abc import abstractmethod, ABC
from typing import Dict

from idact.core.cluster import Cluster
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig


class Environment(ABC):
    """User working environment."""

    @property
    @abstractmethod
    def config(self) -> ClientConfig:
        """Client-side configuration."""
        pass

    @property
    @abstractmethod
    def clusters(self) -> Dict[str, Cluster]:
        """All :class:`.Cluster` objects defined by configuration."""
        pass

    @abstractmethod
    def add_cluster(self,
                    name: str,
                    config: ClusterConfigImpl) -> Cluster:
        """Adds a cluster to config and cluster list.
            Returns the added :class:`.Cluster`.

             :param name:   Cluster name.

             :param config: Client-side cluster config.

        """
        pass

    @abstractmethod
    def remove_cluster(self, name: str):
        """Removes the cluster from config and cluster list.

             :param name:   Cluster name.
        """
        pass

    @abstractmethod
    def set_log_level(self, level: int):
        """Sets the log level for idact.

            See :func:`.set_log_level`.

            :param level: Log level.

        """
        pass

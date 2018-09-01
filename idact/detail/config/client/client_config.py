"""This module contains the implementation of the client config interface."""

from logging import INFO
from typing import Dict, Optional

from idact.core.config import ClusterConfig
from idact.detail.config.validation. \
    validate_cluster_name import validate_cluster_name
from idact.detail.config.validation.validate_log_level \
    import validate_log_level


class ClientConfig:
    """Client-side config.

        :param clusters: Map of cluster config by cluster name.

        :param log_level: Log level, see :func:`.set_log_level`.

    """

    def __init__(self,
                 clusters: Optional[Dict[str, ClusterConfig]] = None,
                 log_level: int = INFO):
        if clusters is None:
            clusters = {}
        self._clusters = {validate_cluster_name(cluster_name): cluster_config
                          for cluster_name, cluster_config in clusters.items()}
        self._log_level = validate_log_level(log_level)

    @property
    def clusters(self) -> Dict[str, ClusterConfig]:
        """Map of cluster config by cluster name."""
        return self._clusters

    @property
    def log_level(self) -> int:
        """Log level for `idact` and Fabric."""
        return self._log_level

    @log_level.setter
    def log_level(self, value: int):
        self._log_level = validate_log_level(value)

    def add_cluster(self,
                    name: str,
                    config: ClusterConfig):
        """Adds a new cluster to config.

            :param name: Cluster name, see validate_cluster_name.
                         Must be unique.

            :param config: Cluster configuration.
        """

        if name in self._clusters:
            raise ValueError("Cluster already added: {}".format(name))

        self._clusters[validate_cluster_name(name)] = config

    def remove_cluster(self, name: str):
        """Removes a new cluster from config.

            :param name: Cluster name.

        """
        self._clusters.pop(name)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

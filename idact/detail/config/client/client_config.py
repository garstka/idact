from typing import Dict, Optional

from idact.detail.config.client. \
    client_cluster_config import ClientClusterConfig
from idact.detail.config.validation. \
    validate_cluster_name import validate_cluster_name


class ClientConfig:
    """Client-side config.

       :param clusters: Cluster connection config.
    """

    def __init__(self,
                 clusters: Optional[Dict[str, ClientClusterConfig]] = None):
        if clusters is None:
            clusters = {}
        self._clusters = {validate_cluster_name(cluster_name): cluster_config
                          for cluster_name, cluster_config in clusters.items()}

    @property
    def clusters(self) -> Dict[str, ClientClusterConfig]:
        """All clusters."""
        return self._clusters

    def add_cluster(self,
                    name: str,
                    config: ClientClusterConfig):
        """Adds a new cluster to config.

            :param name: Cluster name, see validate_cluster_name.
                         Must be unique.

            :param config: Cluster configuration.
        """

        if name in self._clusters:
            raise ValueError("Cluster already added: {}".format(name))

        self._clusters[validate_cluster_name(name)] = config

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

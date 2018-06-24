"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.show_clusters`, :func:`.show_cluster`.
"""

from typing import Dict

from idact.core.cluster import Cluster
from idact.detail.environment.environment_provider import EnvironmentProvider


def show_clusters() -> Dict[str, Cluster]:
    """Returns a dictionary of all defined clusters by name."""
    environment = EnvironmentProvider().environment
    return {key: value for key, value in environment.clusters.items()}


def show_cluster(name: str) -> Cluster:
    """Returns the cluster with this name.

        :param name: Cluster name.
    """
    environment = EnvironmentProvider().environment
    return environment.clusters[name]

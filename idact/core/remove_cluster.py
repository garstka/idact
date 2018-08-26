"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.remove_cluster`.
"""
from idact.detail.environment.environment_provider import EnvironmentProvider


def remove_cluster(name: str):
    """Removes a cluster with this name

        :param name: Name of the cluster to remove
    """
    environment = EnvironmentProvider().environment
    environment.remove_cluster(name=name)

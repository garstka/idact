"""This module contains a function for building the access node host string
    from config."""
from idact.core.config import ClusterConfig


def get_host_string(config: ClusterConfig) -> str:
    """Returns the access node host string for Fabric.

        :param config: Cluster config.
    """
    return "{user}@{host}:{port}".format(user=config.user,
                                         host=config.host,
                                         port=config.port)

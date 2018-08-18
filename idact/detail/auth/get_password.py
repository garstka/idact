"""This module contains a function for getting a password from cache,
    or by prompting the user."""

from getpass import getpass

from idact.detail.auth.get_host_string import get_host_string
from idact.detail.auth.set_password import PasswordCache
from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl


def get_password(config: ClusterConfigImpl) -> str:
    """Obtains the password from user input or password cache.

        :param config: Cluster config.
    """
    if PasswordCache().password is not None:
        return PasswordCache().password

    return getpass("Password for {host_string}: ".format(
        host_string=get_host_string(config=config)))

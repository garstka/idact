"""This module contains a function for getting a password from cache,
    or by prompting the user."""

import getpass

from idact.core.config import ClusterConfig
from idact.detail.auth.get_host_string import get_host_string
from idact.detail.auth.set_password import PasswordCache


def get_password(config: ClusterConfig) -> str:
    """Obtains the password from user input or password cache.

        :param config: Cluster config.
    """
    if PasswordCache().password is not None:
        return PasswordCache().password

    return getpass.getpass("Password for {host_string}: ".format(
        host_string=get_host_string(config=config)))

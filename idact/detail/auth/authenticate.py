from contextlib import contextmanager
from typing import Tuple

from fabric.state import env

from idact.core.auth import AuthMethod
from idact.detail.auth.disable_getpass import disable_getpass
from idact.detail.auth.get_host_string import get_host_string
from idact.detail.auth.get_password import get_password
from idact.detail.auth.install_key import install_key
from idact.detail.auth.install_shared_home_key import install_shared_home_key
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig


def get_host_strings(host: str,
                     config: ClientClusterConfig) -> Tuple[str, str]:
    """Returns host strings for the gateway and target host.
       If the target host is the access node, there is no gateway.
       Otherwise, the access node is the gateway.

        :param host: Connection target.

        :param config: Cluster config.

    """
    gateway = get_host_string(config=config)
    if host == config.host:
        env_gateway = None
        env_host_string = gateway
    else:
        env_gateway = gateway
        env_host_string = "{user}@{host}".format(user=config.user,
                                                 host=host)
    return env_gateway, env_host_string


def install_key_using_password_authentication(config: ClientClusterConfig):
    """Authenticates with a password and tries to install public key.

        :param config: Cluster config.

    """
    access_node = get_host_string(config=config)

    env.password = get_password(config=config)
    saved_gateway, saved_host_string = env.gateway, env.host_string
    env.gateway, env.host_string = None, access_node
    try:
        install_key(config=config)
    finally:
        env.password = None
        env.gateway, env.host_string = saved_gateway, saved_host_string


def install_shared_home_key_using_current_authentication(access_node: str):
    """Installs the key for authentication between the access node,
       and cluster nodes. Uses current authentication.

        :param access_node: The access node.

    """
    saved_password = env.password
    saved_gateway, saved_host_string = env.gateway, env.host_string
    try:
        env.gateway, env.host_string = None, access_node
        install_shared_home_key()
    finally:
        env.password = saved_password
        env.gateway, env.host_string = saved_gateway, saved_host_string


@contextmanager
def authenticate(host: str, config: ClientClusterConfig):
    """Authenticates the user in Fabric.

        :param host: SSH host.

        :param config: Cluster config.
    """
    if config.auth not in [AuthMethod.ASK, AuthMethod.PUBLIC_KEY]:
        raise ValueError("Authentication method not implemented: '{}'.".format(
            config.auth))

    previous_gateway, previous_host = env.gateway, env.host_string
    env.gateway, env.host_string = get_host_strings(host=host, config=config)

    try:
        if config.auth == AuthMethod.ASK:
            env.password = get_password(config=config)
        elif config.auth == AuthMethod.PUBLIC_KEY:
            if config.install_key:
                install_key_using_password_authentication(config=config)
            env.key_filename = config.key

        access_node = get_host_string(config=config)
        if env.host_string != access_node:
            install_shared_home_key_using_current_authentication(
                access_node=access_node)

        with disable_getpass():
            yield
    finally:
        env.gateway, env.host_string = previous_gateway, previous_host

        env.password = None
        if config.auth == AuthMethod.PUBLIC_KEY:
            env.key_filename = None

"""This module contains a context manager that performs node authentication
    according to the configuration."""

from contextlib import contextmanager
from typing import Tuple

from fabric.state import env

from idact.core.config import ClusterConfig
from idact.core.auth import AuthMethod
from idact.detail.auth.disable_getpass import disable_getpass
from idact.detail.auth.get_host_string import get_host_string
from idact.detail.auth.get_password import get_password
from idact.detail.auth.install_key import install_key
from idact.detail.auth.install_shared_home_key import install_shared_home_key
from idact.detail.entry_point.get_entry_point_script_contents import \
    COMPUTE_NODE_AUTHORIZED_KEYS
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger


def get_host_strings(host: str,
                     port: int,
                     config: ClusterConfig) -> Tuple[str, str]:
    """Returns host strings for the gateway and target host.

        If the target host is the access node, there is no gateway.
        Otherwise, the access node is the gateway.

        :param host: Connection target.

        :param port: Connection target port.

        :param config: Cluster config.

    """
    gateway = get_host_string(config=config)
    if host == config.host:
        env_gateway = None
        env_host_string = gateway
    else:
        env_gateway = gateway
        env_host_string = "{user}@{host}:{port}".format(user=config.user,
                                                        host=host,
                                                        port=port)
    return env_gateway, env_host_string


def install_key_using_password_authentication(config: ClusterConfig):
    """Authenticates with a password and tries to install public key,
        using the default authorized_keys file.

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


def install_keys_using_current_authentication(access_node: str,
                                              config: ClusterConfig):
    """Installs keys for authentication between the access node
        and cluster nodes. Uses current authentication.

        :param access_node: The access node.

        :param config: Cluster config.

    """
    saved_password = env.password
    saved_gateway, saved_host_string = env.gateway, env.host_string
    try:
        env.gateway, env.host_string = None, access_node
        install_shared_home_key()
        install_key(config=config,
                    authorized_keys=COMPUTE_NODE_AUTHORIZED_KEYS)
    finally:
        env.password = saved_password
        env.gateway, env.host_string = saved_gateway, saved_host_string


@contextmanager
def authenticate(host: str,
                 port: int,
                 config: ClusterConfig,
                 install_shared_keys: bool = False):
    """Authenticates the user in Fabric.

        :param host: SSH host.

        :param port: SSH port.

        :param config: Cluster config.

        :param install_shared_keys: True, if shared home keys be installed
                                    after authentication.

    """
    if config.auth not in [AuthMethod.ASK, AuthMethod.PUBLIC_KEY]:
        raise NotImplementedError(
            "Authentication method not implemented: '{}'.".format(
                config.auth))

    previous_gateway, previous_host = env.gateway, env.host_string
    env.gateway, env.host_string = get_host_strings(host=host,
                                                    port=port,
                                                    config=config)

    previous_abort_on_prompts = env.abort_on_prompts
    env.shell = "/bin/bash --noprofile -l -c"
    env.key = None
    env.user = config.user
    env.abort_on_prompts = True
    log = get_logger(__name__)
    try:
        if config.auth == AuthMethod.ASK:
            env.password = get_password(config=config)
        elif config.auth == AuthMethod.PUBLIC_KEY:
            if config.install_key:
                with stage_info(log, "Installing key using password"
                                     " authentication."):
                    install_key_using_password_authentication(config=config)
                env.key_filename = config.key
                config.install_key = False
                env.password = None

        access_node = get_host_string(config=config)
        if install_shared_keys:
            with stage_info(log, "Installing key in '%s' for access to compute"
                                 " nodes.",
                            COMPUTE_NODE_AUTHORIZED_KEYS):
                install_keys_using_current_authentication(
                    access_node=access_node,
                    config=config)

        # Key is needed between gateway and compute nodes even when using
        # password-based authentication.
        env.key_filename = config.key
        with disable_getpass():
            yield
    finally:
        env.gateway, env.host_string = previous_gateway, previous_host

        env.password = None
        env.key_filename = None
        env.abort_on_prompts = previous_abort_on_prompts

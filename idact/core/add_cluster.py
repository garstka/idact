"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.add_cluster`.
"""
from typing import Optional, Union

from idact.core.auth import AuthMethod, KeyType
from idact.core.cluster import Cluster
from idact.detail.auth.generate_key import generate_key
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.environment.environment_provider import EnvironmentProvider
from idact.detail.log.get_logger import get_logger


def add_cluster(name: str,
                user: str,
                host: str,
                port: int = 22,
                auth: Optional[AuthMethod] = None,
                key: Union[None, str, KeyType] = None,
                install_key: bool = True,
                disable_sshd: bool = False) -> Cluster:
    """Adds a new cluster.

        :param name:
            Cluster name to identify it by.
        :param user:
            Remote cluster user to log in and run commands as.
        :param host:
            Cluster access node hostname.
        :param port:
            SSH port to access the cluster.
            Default: 22.
        :param auth:
            Authentication method.
            Default: :attr:`.AuthMethod.ASK` (password-based).
        :param key:
            Private key path (if applicable), or key type to generate.
            Default: None
        :param install_key:
            True, if the public key should be installed on the cluster before
            use (if applicable).
            Default: True
        :param disable_sshd:
            Should be set to True, if the cluster allows ssh connection
            to compute nodes out of the box.
            Default: False
       """
    log = get_logger(__name__)
    environment = EnvironmentProvider().environment
    if auth is None:
        log.info("No auth method specified, defaulting to password-based.")
        auth = AuthMethod.ASK

    if auth is AuthMethod.PUBLIC_KEY:
        if isinstance(key, KeyType):
            log.info("Generating public-private key pair.")
            key = generate_key(host=host, key_type=key)
        elif isinstance(key, str):
            pass
        else:
            raise ValueError("Invalid key argument for public key"
                             " authentication.")

    config = ClusterConfigImpl(host=host,
                               port=port,
                               user=user,
                               auth=auth,
                               key=key,
                               install_key=install_key,
                               disable_sshd=disable_sshd)
    return environment.add_cluster(name=name,
                                   config=config)

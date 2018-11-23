"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.add_cluster`.
"""
import os
from typing import Optional, Union, Dict

from idact.core.config import SetupActionsConfig, RetryConfig
from idact.core.auth import AuthMethod, KeyType
from idact.core.cluster import Cluster
from idact.core.retry import Retry
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
                disable_sshd: bool = False,
                setup_actions: Optional[SetupActionsConfig] = None,
                scratch: Optional[str] = None,
                retries: Optional[Dict[Retry, RetryConfig]] = None,
                use_jupyter_lab: bool = True) -> Cluster:
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
        :param setup_actions:
            Commands to run before deployment.
            Default: None
        :param setup_actions:
            Commands to run before deployment.
            Default: None
        :param scratch:
            Absolute path to a high-performance filesystem for temporary
            computation data, or an environment variable that contains it.
            Default: $HOME
        :param retries:
            Retry config by action name.
            Defaults: see :func:`.get_default_retries`.
        :param use_jupyter_lab:
            Use Jupyter Lab instead of Jupyter Notebook.
            Default: True.
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
            key = os.path.expanduser(key)
        else:
            raise ValueError("Invalid key argument for public key"
                             " authentication.")

    config = ClusterConfigImpl(host=host,
                               port=port,
                               user=user,
                               auth=auth,
                               key=key,
                               install_key=install_key,
                               disable_sshd=disable_sshd,
                               setup_actions=setup_actions,
                               scratch=scratch,
                               retries=retries,
                               use_jupyter_lab=use_jupyter_lab)
    return environment.add_cluster(name=name,
                                   config=config)

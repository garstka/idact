"""This module contains functionality for serializing and deserializing config.
"""

from typing import Any, Optional

from idact.core.config import ClusterConfig
from idact.core.auth import AuthMethod
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.config.client.retry_config_serialize \
    import serialize_retries, deserialize_retries
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.config.defaults.provide_defaults_for_retries import \
    provide_defaults_for_retries
from idact.detail.log.get_logger import get_logger


def serialize_client_config_to_json(config: ClientConfig) -> dict:
    """Serializes :class:`.ClientConfig` to json.

        :param config: The object to serialize.
    """

    def get_notebook_defaults(cluster: ClusterConfig) -> dict:
        """Notebook defaults are not in the public interface."""
        assert isinstance(cluster, ClusterConfigImpl)
        return cluster.notebook_defaults

    return {
        'clusters': {
            name: {'host': cluster_config.host,
                   'port': cluster_config.port,
                   'user': cluster_config.user,
                   'auth': str(cluster_config.auth).split('.')[1],
                   'key': cluster_config.key,
                   'installKey': cluster_config.install_key,
                   'disableSshd': cluster_config.disable_sshd,
                   'setupActions': {
                       'jupyter': cluster_config.setup_actions.jupyter,
                       'dask': cluster_config.setup_actions.dask},
                   'scratch': cluster_config.scratch,
                   'notebookDefaults': get_notebook_defaults(cluster_config),
                   'retries': serialize_retries(cluster_config.retries),
                   'useJupyterLab': cluster_config.use_jupyter_lab}
            for name, cluster_config in config.clusters.items()},
        'logLevel': config.log_level}


def use_defaults_in_missing_fields(data: dict) -> bool:
    """Sets missing field values to `None`, so :class:`.ClientConfig`
        and its components can fill out the defaults.
        Returns `True`, if any changes were made.

        :param data: json to deserialize.

    """

    modified = []

    def default(data_to_check: dict, key: str, value: Optional[Any]):
        """Provides a default value for the dict, if it's missing."""
        if key not in data_to_check:
            data_to_check[key] = value
            modified.append(True)

    for cluster in data['clusters'].values():
        for key in ['key',
                    'installKey',
                    'disableSshd',
                    'scratch',
                    'useJupyterLab']:
            default(cluster, key, None)
        default(cluster, 'setupActions', {})
        default(cluster['setupActions'], 'jupyter', None)
        default(cluster['setupActions'], 'dask', None)
        default(cluster, 'notebookDefaults', {})
        default(cluster, 'retries', {})

    return len(modified) != 0


def deserialize_client_config_from_json(data: dict) -> ClientConfig:
    """Deserializes :class:`.ClientConfig` from json.

        :param data: json to deserialize.
    """
    log = get_logger(__name__)

    log.debug("Loaded config: %s", data)
    if use_defaults_in_missing_fields(data=data):
        log.debug("Filled missing fields with None: %s", data)

    clusters = {
        name: ClusterConfigImpl(
            host=value['host'],
            port=value['port'],
            user=value['user'],
            auth=AuthMethod[value['auth']],
            key=value['key'],
            install_key=value['installKey'],
            disable_sshd=value['disableSshd'],
            setup_actions=SetupActionsConfigImpl(
                jupyter=value['setupActions']['jupyter'],
                dask=value['setupActions']['dask']),
            scratch=value['scratch'],
            notebook_defaults=value['notebookDefaults'],
            retries=provide_defaults_for_retries(
                deserialize_retries(value['retries'])),
            use_jupyter_lab=value['useJupyterLab']
        ) for name, value in data['clusters'].items()}
    return ClientConfig(clusters=clusters,
                        log_level=data['logLevel'])

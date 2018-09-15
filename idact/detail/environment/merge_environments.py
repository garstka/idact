import copy

from typing import Dict, Set

from idact.core.config import ClusterConfig
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_impl import EnvironmentImpl


def merge_cluster_configs(local: ClusterConfig,
                          remote: ClusterConfig) -> ClusterConfig:
    """Merges remote cluster config into local cluster config.

        :param local: Local cluster config.

        :param remote: Remote cluster config.

    """
    new_config = copy.deepcopy(remote)
    new_config.install_key = local.install_key
    new_config.key = local.key
    return new_config


def sanitize_cluster_config(remote: ClusterConfig) -> ClusterConfig:
    """Sanitizes remote cluster config for a cluster that is not present
        in local config.

        :param remote: Remote cluster config.

    """
    new_config = copy.deepcopy(remote)
    new_config.install_key = True
    new_config.key = None
    return new_config


def get_common_clusters(local_clusters: Dict[str, ClusterConfig],
                        remote_clusters: Dict[str, ClusterConfig]) -> Set[str]:
    """Returns the cluster names that occur in both sets.

        :param local_clusters: Local cluster set.

        :param remote_clusters: Remote cluster set.

    """
    return {name for name in local_clusters if name in remote_clusters}


def merge_common_clusters(remote_clusters: Dict[str, ClusterConfig],
                          target_clusters: Dict[str, ClusterConfig]):
    """Merges clusters that are in both target and remote cluster sets.

        :param remote_clusters: Remote cluster set.

        :param target_clusters: Local (target) cluster set.

    """
    common_clusters = get_common_clusters(local_clusters=target_clusters,
                                          remote_clusters=remote_clusters)
    for cluster_name in common_clusters:
        local_config = target_clusters[cluster_name]
        remote_config = remote_clusters[cluster_name]
        merged_config = merge_cluster_configs(local=local_config,
                                              remote=remote_config)
        target_clusters[cluster_name] = merged_config


def get_new_clusters(local_clusters: Dict[str, ClusterConfig],
                     remote_clusters: Dict[str, ClusterConfig]) -> Set[str]:
    """Returns the cluster names that occur only in the remote cluster set.

        :param local_clusters: Local cluster set.

        :param remote_clusters: Remote cluster set.

    """
    return {name for name in remote_clusters if name not in local_clusters}


def sanitize_and_add_new_clusters(remote_clusters: Dict[str, ClusterConfig],
                                  target_clusters: Dict[str, ClusterConfig]):
    """Sanitizes clusters that are only in remote config.

        :param remote_clusters: Clusters in remote environment.

        :param target_clusters: Target clusters list.

    """
    new_clusters = get_new_clusters(local_clusters=target_clusters,
                                    remote_clusters=remote_clusters)
    for cluster_name in new_clusters:
        remote_config = remote_clusters[cluster_name]
        sanitized_config = sanitize_cluster_config(remote=remote_config)
        target_clusters[cluster_name] = sanitized_config


def merge_environments(local: Environment,
                       remote: Environment) -> Environment:
    """Merges remote environment into local environment
        Replaces every entry for a given cluster, except machine-specific
        values, like key paths. Adds clusters present only in remote config.

        :param local: Local environment.

        :param remote: Remote environment.

    """
    config = copy.deepcopy(local.config)

    merge_common_clusters(remote_clusters=remote.config.clusters,
                          target_clusters=config.clusters)
    sanitize_and_add_new_clusters(remote_clusters=remote.config.clusters,
                                  target_clusters=config.clusters)

    return EnvironmentImpl(config=config)

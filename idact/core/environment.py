"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.load_environment`, :func:`.save_environment`,
   :func:`.pull_environment`, :func:`.push_environment`.

"""

from typing import Optional

from idact.core.cluster import Cluster
from idact.detail.environment.environment_impl import EnvironmentImpl
from idact.detail.environment.environment_provider import EnvironmentProvider
from idact.detail.environment.environment_remote_serialization import \
    deserialize_environment_from_cluster, serialize_environment_to_cluster
from idact.detail.environment.environment_serialization import \
    serialize_environment_to_file, deserialize_environment_from_file
from idact.detail.environment.merge_environments import merge_environments
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger


def load_environment(path: Optional[str] = None):
    """Loads the environment from file.

        :param path: Path to environment file.
                     Default: IDACT_CONFIG_PATH environment variable,
                     or ~/.idact.conf
    """
    environment = deserialize_environment_from_file(path=path)
    EnvironmentProvider().environment = environment


def save_environment(path: Optional[str] = None):
    """Saves the environment to file.

        :param path: Path to environment file.
                     Default: IDACT_CONFIG_PATH environment variable,
                     or ~/.idact.conf
    """
    environment = EnvironmentProvider().environment
    serialize_environment_to_file(environment=environment,
                                  path=path)


def pull_environment(cluster: Cluster,
                     path: Optional[str] = None):
    """Merges the current environment with the environment on cluster.

        :param cluster: Cluster to pull the environment from.

        :param path: Path to remote environment file.
                     Default: Remote IDACT_CONFIG_PATH environment variable,
                     or ~/.idact.conf

    """
    log = get_logger(__name__)
    with stage_info(log, "Pulling the environment from cluster."):
        remote_environment = deserialize_environment_from_cluster(
            cluster=cluster,
            path=path)
        local_environment = EnvironmentProvider().environment
        merged_environment = merge_environments(local=local_environment,
                                                remote=remote_environment)
        EnvironmentProvider().environment = merged_environment


def push_environment(cluster: Cluster, path: Optional[str] = None):
    """Merges the environment on the cluster with the current environment.

        :param cluster: Cluster to push the environment to.

        :param path: Path to remote environment file.
                     Default: Remote IDACT_CONFIG_PATH environment variable,
                     or ~/.idact.conf
    """
    log = get_logger(__name__)
    with stage_info(log, "Pushing the environment to cluster."):
        try:
            remote_environment = deserialize_environment_from_cluster(
                cluster=cluster,
                path=path)
        except RuntimeError:
            log.info("Remote environment is missing, current environment will"
                     " be copied to cluster.")
            log.debug("Exception", exc_info=1)
            remote_environment = EnvironmentImpl()

        local_environment = EnvironmentProvider().environment
        merged_environment = merge_environments(local=remote_environment,
                                                remote=local_environment)
        serialize_environment_to_cluster(environment=merged_environment,
                                         cluster=cluster,
                                         path=path)

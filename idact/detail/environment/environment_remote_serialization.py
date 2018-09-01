"""This module contains functions for serializing and deserializing
    the environment."""

from typing import Optional

import fabric.decorators

from idact.core.nodes import Node
from idact.core.cluster import Cluster
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_text_serialization import \
    deserialize_environment, serialize_environment
from idact.detail.helper.get_remote_file import get_remote_file
from idact.detail.helper.put_remote_file import put_remote_file
from idact.detail.nodes.node_internal import NodeInternal

DEFAULT_REMOTE_ENVIRONMENT_PATH = '~/.idact.conf'


def get_remote_environment_path(node: Node,
                                path: Optional[str]) -> str:
    """Returns the remote path to config file, or Raises a RuntimeError.

        :param path: Optional remote path.

    """
    if path is None:
        path = node.run("printenv IDACT_CONFIG_PATH || echo {}".format(
            DEFAULT_REMOTE_ENVIRONMENT_PATH))

    path = node.run("realpath {}".format(path))
    if not path:
        raise RuntimeError("Unable to determine remote config path.")

    return path


def serialize_environment_to_cluster(environment: Environment,
                                     cluster: Cluster,
                                     path: Optional[str]):
    """Dumps the environment to remote file.

        See :func:`.push_environment`.

        :param environment: Environment to save.

        :param cluster: Cluster to push the environment to.

        :param path: Remote file path.
                     Default: IDACT_CONFIG_PATH environment variable,
                              or ~/.idact.conf

    """
    node = cluster.get_access_node()
    assert isinstance(node, NodeInternal)
    path = get_remote_environment_path(node=node, path=path)

    file_contents = serialize_environment(environment)

    @fabric.decorators.task
    def file_upload_task():
        put_remote_file(remote_path=path, contents=file_contents)

    node.run_task(task=file_upload_task)


def deserialize_environment_from_cluster(cluster: Cluster,
                                         path: Optional[
                                             str] = None) -> Environment:  # noqa, pylint: disable=line-too-long,bad-whitespace
    """Loads the environment from remote file.

        See :func:`.pull_environment`.

        :param cluster: Cluster to pull the environment from.

        :param path: Remote file path.
                     Default: Remote IDACT_CONFIG_PATH environment variable,
                              or ~/.idact.conf

    """
    node = cluster.get_access_node()
    assert isinstance(node, NodeInternal)
    path = get_remote_environment_path(node=node, path=path)

    @fabric.decorators.task
    def file_download_task():
        return get_remote_file(remote_path=path)

    file_contents = node.run_task(task=file_download_task)
    return deserialize_environment(text=file_contents)

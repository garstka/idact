"""This module contains a function for creating a runtime dir on a cluster."""

from idact.detail.helper.get_random_file_name import get_random_file_name
from idact.detail.nodes.node_internal import NodeInternal

DEPLOYMENT_ID_LENGTH = 32
DEPLOYMENT_RUNTIME_DIR_FORMAT = "~/.idact/runtime/{deployment_id}"


def create_runtime_dir(node: NodeInternal) -> str:
    """Creates and returns the path to a random dir on node.

        The created dir is a subdir of `~/.idact/runtime`, see
        :attr:`.DEPLOYMENT_RUNTIME_DIR_FORMAT`.

        :param node: Node to create a runtime dir on.

    """
    deployment_id = get_random_file_name(length=DEPLOYMENT_ID_LENGTH)
    formatted_runtime_dir = DEPLOYMENT_RUNTIME_DIR_FORMAT.format(
        deployment_id=deployment_id)

    node.run('mkdir -p {}'.format(formatted_runtime_dir))
    node.run('chmod 700 {}'.format(formatted_runtime_dir))
    runtime_dir = node.run("readlink -vf {}".format(formatted_runtime_dir))

    return runtime_dir

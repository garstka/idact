import json

from idact.core.node import Node
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.helper.file_exists_on_node import file_exists_on_node
from idact.detail.helper.get_remote_file import get_file_from_node
from idact.detail.helper.put_remote_file import put_file_on_node
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal

DEPLOYMENT_DEFINITIONS_PATH = '~/.idact'
DEPLOYMENT_DEFINITIONS_FILENAME = '.deployments'


def get_deployment_definitions_parent_path(node: Node) -> str:
    """Returns the parent dir path of the deployment definitions file.

        :param node: Node to run commands on.

    """
    return node.run("readlink -vf {}".format(DEPLOYMENT_DEFINITIONS_PATH))


def get_deployment_definitions_file_path(node: Node) -> str:
    """Returns the path to the deployment definitions file.

        :param node: Node to run commands on.

    """
    return node.run("readlink -vf {}/{}".format(
        DEPLOYMENT_DEFINITIONS_PATH,
        DEPLOYMENT_DEFINITIONS_FILENAME))


def deployment_definitions_file_exists(node: NodeInternal) -> bool:
    """Returns True, if the deployment definitions file exists.

        :param node: Node to run commands on.

    """
    path = get_deployment_definitions_file_path(node=node)
    return file_exists_on_node(node=node,
                               path=path)


# pylint: disable=bad-continuation
def deserialize_deployment_definitions_from_cluster(
    node: NodeInternal) -> DeploymentDefinitions:  # noqa
    """Downloads deployment definitions from the cluster.

        :param node: Node to deserialize deployment definitions from.

    """
    log = get_logger(__name__)
    with stage_debug(log, "Deserializing deployment definitions"
                          " from cluster."):
        path = get_deployment_definitions_file_path(node=node)
        file_contents = get_file_from_node(
            node=node,
            remote_path=path)

        serialized = json.loads(file_contents)
        return DeploymentDefinitions.deserialize(serialized=serialized)


# pylint: disable=bad-continuation
def serialize_deployment_definitions_to_cluster(
    node: NodeInternal,
    deployments: DeploymentDefinitions):  # noqa
    """Uploads deployment definitions to the cluster, replacing
        any definitions file already there.

        :param node: Node to serialize definitions to.

        :param deployments: Deployments to upload.

    """
    log = get_logger(__name__)
    with stage_debug(log, "Serializing deployment definitions to cluster."):
        serialized = deployments.serialize()
        file_contents = json.dumps(serialized, sort_keys=True, indent=4)
        parent_path = get_deployment_definitions_parent_path(node=node)
        node.run("mkdir -p {}".format(parent_path))
        node.run("chmod 700 {}".format(parent_path))
        path = get_deployment_definitions_file_path(node=node)
        put_file_on_node(node=node,
                         remote_path=path,
                         contents=file_contents)


def remove_serialized_deployment_definitions(node: NodeInternal):
    """Removes the deployment definitions file, if it exists.

        :param node: Node to run commands on.
    """
    path = get_deployment_definitions_file_path(node=node)
    node.run("rm -f '{path}'".format(path=path))

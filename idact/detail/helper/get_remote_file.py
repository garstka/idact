"""This module contains a function for downloading a file from cluster
    in a Fabric task."""

from io import BytesIO

import fabric.decorators
from fabric.operations import get

from idact.detail.nodes.node_internal import NodeInternal


def get_remote_file(remote_path: str) -> str:
    """Fetches remote file as a string.

        Expects authentication to have been performed already.

        :param remote_path: Remote file path.

    """
    file = BytesIO()
    get(remote_path, file)
    contents = file.getvalue().decode()
    return contents


def get_file_from_node(node: NodeInternal,
                       remote_path: str) -> str:
    """Runs a task on the node that downloads a file and returns its contents.

        :param node: Node to download the file from.

        :param remote_path: Remote file path.

    """

    @fabric.decorators.task
    def file_upload_task():
        return get_remote_file(remote_path=remote_path)

    return node.run_task(task=file_upload_task)

"""This module contains a function for downloading a file from cluster
    in a Fabric task."""

from io import BytesIO

import fabric.decorators
from fabric.operations import put

from idact.detail.nodes.node_internal import NodeInternal


def put_remote_file(remote_path: str, contents: str):
    """Uploads a remote file from string with r/w user permissions only.

        Expects authentication to have been performed already.

        :param remote_path: Remote file path.

        :param contents: File contents.

    """
    file = BytesIO(contents.encode())
    put(file, remote_path, mode=0o600)


def put_file_on_node(node: NodeInternal,
                     remote_path: str,
                     contents: str):
    """Runs a task on the node that uploads a file.

        :param node: Node to upload the file to.

        :param remote_path: Remote file path.

        :param contents: File contents.

    """

    @fabric.decorators.task
    def file_upload_task():
        put_remote_file(remote_path=remote_path,
                        contents=contents)

    node.run_task(task=file_upload_task)

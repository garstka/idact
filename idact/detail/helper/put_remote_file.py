"""This module contains a function for downloading a file from cluster
    in a Fabric task."""

from io import BytesIO

import fabric.decorators
from fabric.operations import put

from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.log.get_logger import get_logger
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
    log = get_logger(__name__)
    with stage_debug(log, "Putting file on node %s: %s",
                     node.host, remote_path):
        @fabric.decorators.task
        def file_upload_task():
            with capture_fabric_output_to_log():
                put_remote_file(remote_path=remote_path,
                                contents=contents)

        node.run_task(task=file_upload_task)

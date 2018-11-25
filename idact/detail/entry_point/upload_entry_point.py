"""This module contains a function for uploading an entry point script."""

from io import BytesIO

import fabric.tasks
from fabric.contrib.files import exists
import fabric.decorators
from fabric.operations import run, put

from idact.detail.helper.get_random_file_name import get_random_file_name
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal

ENTRY_POINT_LOCATION = "~/.idact/entry_points"
ENTRY_POINT_FILE_NAME_LENGTH = 32


def upload_entry_point(contents: str,
                       node: NodeInternal) -> str:
    """Uploads the entry point script and returns its path.

        :param contents: Script contents.

        :param node: Node to upload the entry point to.

    """
    log = get_logger(__name__)

    result = []

    @fabric.decorators.task
    def task():
        """Creates the entry point dir and file.
            Fails if it couldn't be created."""
        with capture_fabric_output_to_log():
            run("mkdir -p {entry_point_location}".format(
                entry_point_location=ENTRY_POINT_LOCATION))
            run("chmod 700 {entry_point_location}".format(
                entry_point_location=ENTRY_POINT_LOCATION))

            file_name = get_random_file_name(
                length=ENTRY_POINT_FILE_NAME_LENGTH)
            file_path = run("echo {entry_point_location}/{file_name}".format(
                entry_point_location=ENTRY_POINT_LOCATION,
                file_name=file_name))
            file_exists = exists(file_path)

        if file_exists:
            log.warning("Overwriting randomly named entry point file:"
                        " %s", file_path)

        with stage_debug(log, "Uploading the entry point script."):
            with capture_fabric_output_to_log():
                real_path = run("echo {file_path}".format(file_path=file_path))
                file = BytesIO(contents.encode('ascii'))
                put(file, real_path, mode=0o700)

        with stage_debug(log, "Checking the entry point script was uploaded."):
            with capture_fabric_output_to_log():
                run("cat {real_path} > /dev/null".format(
                    real_path=real_path))
        result.append(real_path)

    node.run_task(task)

    return result[0]

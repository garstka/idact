"""This module contains a function for fetching a file with sshd deployment
    ports from cluster."""

import fabric.decorators
import fabric.tasks
from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.operations import run

from idact.core.config import ClusterConfig
from idact.detail.auth.authenticate import authenticate
from idact.detail.entry_point.sshd_port_info \
    import PORT_INFO_DIR_NAME_FORMAT, PORT_INFO_LOCATION
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.log.get_logger import get_logger


def fetch_port_info(allocation_id: int,
                    config: ClusterConfig) -> str:
    """Fetches the contents of the directory containing sshd deployment ports.
        Returns an empty string, if not found.

        :param allocation_id: Allocation id, e.g. Slurm job id.

        :param config: Cluster config.

    """
    log = get_logger(__name__)

    result = []

    @fabric.decorators.task
    def task():
        """Reads the port info file if it exists."""
        port_info_dir = PORT_INFO_DIR_NAME_FORMAT.format(
            allocation_id=allocation_id)

        dir_path = "{port_info_location}/{port_info_dir}".format(
            port_info_location=PORT_INFO_LOCATION,
            port_info_dir=port_info_dir)

        with capture_fabric_output_to_log():
            dir_exists = exists(dir_path)

        if dir_exists:
            with capture_fabric_output_to_log():
                with cd(dir_path):
                    files = run("echo *", pty=False)
                    result.append(files)
        else:
            log.warning("Port info directory not found.")
            result.append("")

    with raise_on_remote_fail(exception=RuntimeError):
        with authenticate(host=config.host,
                          port=config.port,
                          config=config):
            fabric.tasks.execute(task)

    return result[0]

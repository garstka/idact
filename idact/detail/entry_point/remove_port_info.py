"""This module contains a function for removing a file with sshd deployment
    ports from cluster."""

import fabric.decorators
import fabric.tasks
from fabric.operations import run

from idact.core.config import ClusterConfig
from idact.detail.auth.authenticate import authenticate
from idact.detail.entry_point.sshd_port_info \
    import PORT_INFO_DIR_NAME_FORMAT, PORT_INFO_LOCATION
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log


def remove_port_info(allocation_id: int,
                     config: ClusterConfig):
    """Removes the file containing sshd deployment ports.

        :param allocation_id: Allocation id, e.g. Slurm job id.

        :param config: Cluster config.

    """

    port_info_dir = PORT_INFO_DIR_NAME_FORMAT.format(
        allocation_id=allocation_id)

    dir_path = "{port_info_location}/{port_info_dir}".format(
        port_info_location=PORT_INFO_LOCATION,
        port_info_dir=port_info_dir)

    @fabric.decorators.task
    def task():
        with capture_fabric_output_to_log():
            run("rm -f {dir_path}/*"
                " && rmdir {dir_path}"
                " || exit 0".format(dir_path=dir_path))

    with raise_on_remote_fail(exception=RuntimeError):
        with authenticate(host=config.host,
                          port=config.port,
                          config=config):
            fabric.tasks.execute(task)

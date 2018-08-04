from io import BytesIO

import fabric.decorators
import fabric.tasks
from fabric.contrib.files import exists
from fabric.operations import get, run

from idact.detail.auth.authenticate import authenticate
from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl
from idact.detail.entry_point.sshd_port_info import PORT_INFO_FILE_FORMAT, \
    PORT_INFO_LOCATION
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.log.get_logger import get_logger


def fetch_port_info(allocation_id: int,
                    config: ClusterConfigImpl) -> str:
    """Fetches the contents of file containing sshd deployment ports.
        Returns an empty string, if not found.

        :param allocation_id: Allocation id, e.g. Slurm job id.

        :param config: Cluster config.

    """
    log = get_logger(__name__)

    result = []

    @fabric.decorators.task
    def task():
        port_info_file = PORT_INFO_FILE_FORMAT.format(
            allocation_id=allocation_id)

        file_path = "{port_info_location}/{port_info_file}".format(
            port_info_location=PORT_INFO_LOCATION,
            port_info_file=port_info_file)

        if exists(file_path):
            port_info_fd = BytesIO()
            get(file_path, port_info_fd)
            contents = port_info_fd.getvalue().decode('ascii')
            run("rm -f {file_path} || exit 0".format(file_path=file_path))
            result.append(contents)
        else:
            log.warning("Port info file not found.")
            result.append("")

    with raise_on_remote_fail(exception=RuntimeError):
        with authenticate(host=config.host,
                          port=config.port,
                          config=config):
            fabric.tasks.execute(task)

    return result[0]

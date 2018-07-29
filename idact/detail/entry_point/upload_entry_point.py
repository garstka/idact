from io import BytesIO

import fabric.tasks
from fabric.contrib.files import exists
import fabric.decorators
from fabric.operations import run, put

from idact.detail.auth.authenticate import authenticate
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.helper.get_random_file_name import get_random_file_name
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.log.get_logger import get_logger

ENTRY_POINT_LOCATION = "~/.idact/entry_points"
ENTRY_POINT_FILE_NAME_LENGTH = 32


def upload_entry_point(contents: str,
                       config: ClientClusterConfig) -> str:
    """Uploads the entry point file and returns its path.

        :param contents: Script contents.

        :param config: Cluster config.

    """
    log = get_logger(__name__)

    result = []

    @fabric.decorators.task
    def task():
        run("mkdir -p {entry_point_location}".format(
            entry_point_location=ENTRY_POINT_LOCATION))

        file_name = get_random_file_name(
            length=ENTRY_POINT_FILE_NAME_LENGTH)
        file_path = run("echo {entry_point_location}/{file_name}".format(
            entry_point_location=ENTRY_POINT_LOCATION,
            file_name=file_name))

        if exists(file_path):
            log.warning("Overwriting randomly named entry point file:"
                        " %s", file_path)

        real_path = run("echo {file_path}".format(file_path=file_path))
        file = BytesIO(contents.encode('ascii'))
        put(file, real_path, mode=0o700)
        result.append(real_path)

    with raise_on_remote_fail(exception=RuntimeError):
        with authenticate(host=config.host,
                          port=config.port,
                          config=config):
            fabric.tasks.execute(task)

    return result[0]

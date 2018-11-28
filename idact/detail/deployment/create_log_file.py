from idact.core.node import Node
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger


def create_log_file(node: Node, runtime_dir: str) -> str:
    """Creates a log file in the runtime dir.

        :param node: Node to create the log file on.

        :param runtime_dir: Runtime dir path.

    """
    log = get_logger(__name__)
    log_file = '{runtime_dir}/log'.format(runtime_dir=runtime_dir)
    with stage_debug(log, "Creating log file: '%s'.", log_file):
        node.run("touch '{}'".format(log_file))
        return log_file

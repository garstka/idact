import fabric.decorators
from fabric.contrib.files import exists

from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.nodes.node_internal import NodeInternal


def file_exists_on_node(node: NodeInternal,
                        path: str):
    """Returns True, if the file exists on the node.

        :param node: Node to run commands on.

        :param path: File path.

    """

    @fabric.decorators.task
    def task():
        with capture_fabric_output_to_log():
            return exists(path)

    return node.run_task(task=task)

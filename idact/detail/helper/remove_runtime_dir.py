from idact.core.nodes import Node
from idact.detail.log.get_logger import get_logger


def remove_runtime_dir(node: Node, runtime_dir: str):
    """Removes a runtime dir for deployment.
       Removes all files in it that do not start with a dot.
       Does not remove nested directories.
       On failure, produces a warning.

        :param node: Node to run commands on.

        :param path: Path to the deployment dir.
    """
    try:
        node.run("rm -f {runtime_dir}/*"
                 " && rmdir {runtime_dir}".format(runtime_dir=runtime_dir))
    except RuntimeError:
        log = get_logger(__name__)
        log.warning("Failed to remove runtime dir: '%s'.", runtime_dir)
        log.exception("Failed to remove runtime dir due to exception.")

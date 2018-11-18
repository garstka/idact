"""This module contains functions for removing a runtime dir."""

from contextlib import contextmanager

from idact.core.nodes import Node
from idact.detail.log.get_logger import get_logger


def remove_runtime_dir(node: Node, runtime_dir: str):
    """Removes a runtime dir for deployment.

        Removes all files in it that do not start with a dot.
        Does not remove nested directories. On failure, produces a warning.

        :param node: Node to run commands on.

        :param runtime_dir: Path to the deployment dir.

    """
    try:
        node.run("rm -f {runtime_dir}/*"
                 " && rmdir {runtime_dir}".format(runtime_dir=runtime_dir))
    except RuntimeError:
        log = get_logger(__name__)
        log.warning("Failed to remove runtime dir: '%s'.", runtime_dir)
        log.debug("Failed to remove runtime dir due to exception.", exc_info=1)


@contextmanager
def remove_runtime_dir_on_failure(node: Node, runtime_dir: str):
    """A context manager that removes the runtime dir, when an exception
        is thrown.

        :param node: Node to run commands on.

        :param runtime_dir: Path to the runtime dir.

    """
    try:
        yield
    except Exception as e:  # noqa, pylint: disable=broad-except
        remove_runtime_dir(node=node, runtime_dir=runtime_dir)
        raise e


@contextmanager
def remove_runtime_dir_on_exit(node: Node, runtime_dir: str):
    """A context manager that removes the runtime dir on context exit.

        :param node: Node to run commands on.

        :param runtime_dir: Path to the runtime dir.

    """
    try:
        yield
    finally:
        remove_runtime_dir(node=node, runtime_dir=runtime_dir)

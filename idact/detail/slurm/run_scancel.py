"""This module contains a function for running scancel on a node."""

from idact.core.nodes import Node


def run_scancel(job_id: int,
                node: Node):
    """Cancels the job by running `scancel`.

        :param job_id: Job id to cancel

        :param node:   Node to run scancel on.

    """

    node.run("scancel {}".format(int(job_id)))

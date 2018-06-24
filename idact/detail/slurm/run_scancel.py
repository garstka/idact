from idact.core.nodes import Node


def run_scancel(job_id: int,
                node: Node):
    """Cancels the job.

        :param job_id: Job id to cancel

        :param node:   Node to run scancel on.
    """

    node.run("scancel {}".format(int(job_id)))

from idact.core.nodes import Node


def run_scancel(job_id: int,
                node: Node):
    """Runs 'scancel job_id' on the given node."""

    node.run("scancel {}".format(int(job_id)))

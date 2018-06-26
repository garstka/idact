import datetime
from time import sleep
from typing import Optional, List

from idact.detail.allocation.allocation import Allocation
from idact.core.nodes import Node
from idact.detail.helper.utc_now import utc_now
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.slurm.run_scancel import run_scancel
from idact.detail.slurm.run_squeue import run_squeue


class SlurmAllocation(Allocation):
    """Corresponds to a Slurm job.

        :param job_id: Slurm job ID.

        :param access_node: Access node for the cluster on which the job
                            was requested.

        :param nodes: Nodes to update with information after the job state
                      changes to RUNNING.
    """

    def __init__(self,
                 job_id: int,
                 access_node: Node,
                 nodes: List[NodeImpl]):
        self._job_id = job_id
        self._access_node = access_node
        self._nodes = nodes

    def wait(self, timeout: Optional[float]):
        interval = 3
        end = None
        if timeout is not None:
            end = utc_now() + datetime.timedelta(seconds=timeout)
        while True:
            squeue = run_squeue(node=self._access_node)

            try:
                job = squeue[self._job_id]
            except KeyError as e:
                raise RuntimeError("Unable to obtain information "
                                   "about the allocation.") from e

            if job.state in ['PENDING', 'CONFIGURING']:
                if end is not None and utc_now() >= end:
                    raise TimeoutError("Timed out while waiting "
                                       "for allocation.")
                sleep(interval)
                continue
            if job.state != 'RUNNING':
                message = ("Unable to wait: allocation entered unsupported "
                           "or failing state: '{}'")
                raise RuntimeError(message.format(job.state))

            for host, node in zip(job.node_list, self._nodes):
                node.make_allocated(host=host,
                                    allocated_until=job.end_time)
            return

    def cancel(self):
        run_scancel(job_id=self._job_id,
                    node=self._access_node)
        for node in self._nodes:
            node.make_cancelled()

    def running(self) -> bool:
        squeue = run_squeue(node=self._access_node)
        return (self._job_id in squeue and
                squeue[self._job_id].state == 'RUNNING')

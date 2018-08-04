import datetime
from time import sleep
from typing import Optional, List

from idact.detail.allocation.allocation import Allocation
from idact.detail.entry_point.fetch_port_info import fetch_port_info
from idact.detail.entry_point.sshd_port_info import SshdPortInfo
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
                      changes to `RUNNING`.

        :param entry_point_script_path: Entry point file to remove after
                                        job starts.

    """

    def __init__(self,
                 job_id: int,
                 access_node: NodeImpl,
                 nodes: List[NodeImpl],
                 entry_point_script_path: str):
        self._job_id = job_id
        self._access_node = access_node
        self._nodes = nodes
        self._entry_point_script_path = entry_point_script_path

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
            try:
                if job.state != 'RUNNING':
                    message = ("Unable to wait: allocation entered unsupported"
                               " or failing state: '{}'")
                    raise RuntimeError(message.format(job.state))

                port_info_contents = fetch_port_info(
                    allocation_id=self._job_id,
                    config=self._access_node.config)
                port_info = SshdPortInfo(contents=port_info_contents)
                for host, node in zip(job.node_list, self._nodes):
                    node.make_allocated(host=host,
                                        port=port_info.get_port(host=host),
                                        allocated_until=job.end_time)
            finally:
                self._access_node.run("rm -f {entry_point_script_path}".format(
                    entry_point_script_path=self._entry_point_script_path))
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

"""This module contains the implementation of the allocation interface
    for Slurm."""

import datetime
from time import sleep
from typing import Optional, List

from idact.detail.allocation.allocation import Allocation
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.allocation.finalize_allocation import finalize_allocation
from idact.detail.helper.stage_info import stage_info
from idact.detail.helper.utc_now import utc_now
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.serialization.serializable_types import SerializableTypes
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

        :param parameters: Allocation parameters.

        :param done_waiting: Already waited for allocation.

    """

    def __init__(self,
                 job_id: int,
                 access_node: NodeInternal,
                 nodes: List[NodeImpl],
                 entry_point_script_path: str,
                 parameters: AllocationParameters,
                 done_waiting: bool = False):
        self._job_id = job_id
        self._access_node = access_node
        self._nodes = nodes
        self._entry_point_script_path = entry_point_script_path
        self._parameters = parameters
        self._done_waiting = done_waiting

    def wait(self, timeout: Optional[float]):
        log = get_logger(__name__)
        interval = 3
        end = None
        log.debug("Waiting for allocation of job %d...", self._job_id)
        if timeout is not None:
            end = utc_now() + datetime.timedelta(seconds=timeout)

        if self._done_waiting:
            raise RuntimeError("Already waited.")

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
                log.info("Still pending or configuring...")
                sleep(interval)
                continue
            try:
                if job.state != 'RUNNING':
                    message = ("Unable to wait: allocation entered unsupported"
                               " or failing state: '{}'")
                    raise RuntimeError(message.format(job.state))

                self._done_waiting = True
                finalize_allocation(allocation_id=self._job_id,
                                    hostnames=job.node_list,
                                    nodes=self._nodes,
                                    parameters=self._parameters,
                                    allocated_until=job.end_time,
                                    config=self._access_node.config)
            finally:
                self._access_node.run("rm -f {entry_point_script_path}".format(
                    entry_point_script_path=self._entry_point_script_path))
            break

    def cancel(self):
        log = get_logger(__name__)
        with stage_info(log, "Cancelling job %d.", self._job_id):
            run_scancel(job_id=self._job_id,
                        node=self._access_node)
            for node in self._nodes:
                node.make_cancelled()

    def running(self) -> bool:
        squeue = run_squeue(node=self._access_node)
        return (self._job_id in squeue and
                squeue[self._job_id].state == 'RUNNING')

    @property
    def waited(self) -> bool:
        return self._done_waiting

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.SLURM_ALLOCATION),
                'job_id': self._job_id,
                'entry_point_script_path': self._entry_point_script_path,
                'parameters': self._parameters.serialize(),
                'done_waiting': self._done_waiting}

    @staticmethod
    def deserialize(access_node: NodeInternal,
                    nodes: List[NodeImpl],
                    serialized: dict) -> 'SlurmAllocation':
        try:
            assert serialized['type'] == str(
                SerializableTypes.SLURM_ALLOCATION)
            return SlurmAllocation(
                job_id=serialized['job_id'],
                access_node=access_node,
                nodes=nodes,
                entry_point_script_path=serialized['entry_point_script_path'],
                parameters=AllocationParameters.deserialize(
                    serialized['parameters']),
                done_waiting=serialized['done_waiting'])
        except KeyError as e:
            raise RuntimeError("Unable to serialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "SlurmAllocation(job_id={job_id})".format(job_id=self._job_id)

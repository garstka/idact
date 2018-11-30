"""This module contains a function for allocating Slurm nodes."""

from idact.core.config import ClusterConfig
from idact.core.nodes import Nodes
from idact.core.retry import Retry
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.get_access_node import get_access_node
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.nodes_impl import NodesImpl
from idact.detail.slurm.run_sbatch import run_sbatch
from idact.detail.slurm.run_scancel import run_scancel
from idact.detail.slurm.run_squeue import run_squeue
from idact.detail.slurm.sbatch_arguments import SbatchArguments
from idact.detail.slurm.slurm_allocation import SlurmAllocation
from idact.detail.slurm.squeue_result import SqueueResult


def allocate_slurm_nodes(parameters: AllocationParameters,
                         config: ClusterConfig) -> Nodes:
    """Tries to allocate nodes using Slurm.

       :param parameters:   Allocation parameters.

       :param config: Config for the cluster to allocate nodes on.

    """
    args = SbatchArguments(params=parameters)

    log = get_logger(__name__)
    with stage_debug(log, "Executing sbatch on access node."):
        access_node = get_access_node(config=config)
        job_id, entry_point_script_path = run_sbatch(args=args,
                                                     node=access_node)

    def run_squeue_task() -> SqueueResult:
        job_squeue = run_squeue(node=access_node)
        return job_squeue[job_id]

    try:
        with stage_debug(log, "Obtaining info about job %d using squeue.",
                         job_id):
            job = retry_with_config(run_squeue_task,
                                    name=Retry.SQUEUE_AFTER_SBATCH,
                                    config=config)
    except Exception as e:  # noqa, pylint: disable=broad-except
        run_scancel(job_id=job_id, node=access_node)
        raise RuntimeError("Unable to obtain job info"
                           " after allocation.") from e

    node_count = job.node_count
    nodes = [NodeImpl(config=config) for _ in range(node_count)]

    allocation = SlurmAllocation(
        job_id=job_id,
        access_node=access_node,
        nodes=nodes,
        entry_point_script_path=entry_point_script_path,
        parameters=parameters)

    return NodesImpl(nodes=nodes,
                     allocation=allocation)

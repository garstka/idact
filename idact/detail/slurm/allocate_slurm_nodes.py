"""This module contains a function for allocating Slurm nodes."""

from time import sleep

from idact.core.config import ClusterConfig
from idact.core.nodes import Nodes
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.nodes.get_access_node import get_access_node
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.nodes_impl import NodesImpl
from idact.detail.slurm.run_sbatch import run_sbatch
from idact.detail.slurm.run_scancel import run_scancel
from idact.detail.slurm.run_squeue import run_squeue
from idact.detail.slurm.sbatch_arguments import SbatchArguments
from idact.detail.slurm.slurm_allocation import SlurmAllocation


def allocate_slurm_nodes(parameters: AllocationParameters,
                         config: ClusterConfig) -> Nodes:
    """Tries to allocate nodes using Slurm.

       :param parameters:   Allocation parameters.

       :param config: Config for the cluster to allocate nodes on.

    """
    args = SbatchArguments(params=parameters)

    access_node = get_access_node(config=config)
    print(str(access_node))
    assert str(access_node) == repr(access_node)

    job_id, entry_point_script_path = run_sbatch(args=args,
                                                 node=access_node)

    squeue_tries = range(0, 3)
    interval = 3
    job = None
    for _ in squeue_tries:
        try:
            job_squeue = run_squeue(node=access_node)
            job = job_squeue[job_id]
        except KeyError:
            sleep(interval)

    if job is None:
        run_scancel(job_id=job_id, node=access_node)
        raise RuntimeError("Unable to obtain job info after allocation.")

    node_count = job.node_count
    nodes = [NodeImpl(config=config) for _ in range(0, node_count)]

    allocation = SlurmAllocation(
        job_id=job_id,
        access_node=access_node,
        nodes=nodes,
        entry_point_script_path=entry_point_script_path,
        parameters=parameters)

    return NodesImpl(nodes=nodes,
                     allocation=allocation)

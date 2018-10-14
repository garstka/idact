"""This module contains functionality for running sbatch on a node."""

import shlex

from typing import Optional, Dict, Tuple

from idact.core.config import ClusterConfig
from idact.detail.entry_point.get_entry_point_script_contents \
    import get_entry_point_script_contents
from idact.detail.entry_point.upload_entry_point import upload_entry_point
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.slurm.sbatch_arguments import SbatchArguments


def format_args(args: Dict[str, Optional[str]]) -> str:
    """Quotes and joins arguments.

        :param args: Arguments to process.

    """
    argument_list = []
    for key, value in sorted(args.items()):
        argument_list.append(key)
        if value is not None:
            argument_list.append(value)

    quoted = ' '.join([shlex.quote(arg) for arg in argument_list])
    return quoted


def format_sbatch_allocation_request(args: SbatchArguments,
                                     entry_point_script: str) -> str:
    """Formats sbatch command from arguments.

        :param args: Arguments to append.

        :param entry_point_script: Entry point script path

    """
    quoted_native = format_args(args=args.native_args)
    quoted = format_args(args=args.args)

    final = ("sbatch"
             " {quoted_native}"
             " {quoted}"
             " --tasks-per-node=1"  # One /bin/bash -c ... per node.
             " --parsable"
             " --output=/dev/null"
             " --wrap='export IDACT_ALLOCATION_ID=$SLURM_JOB_ID"
             " ; srun {entry_point_script}'") \
        .format(quoted_native=quoted_native,
                quoted=quoted,
                entry_point_script=entry_point_script)
    return final


def prepare_sbatch_allocation_request(args: SbatchArguments,
                                      config: ClusterConfig,
                                      node: NodeInternal) -> \
    Tuple[str, str]:  # noqa
    """Uploads the entry point script and returns the formatted sbatch
        command.

        :param args: Arguments for sbatch.

        :param config: Cluster config.

        :param node: Node to upload entry point to.

    """
    log = get_logger(__name__)
    entry_point_script_contents = \
        get_entry_point_script_contents(config=config)
    log.debug("Entry point script contents: %s", entry_point_script_contents)

    entry_point_script = upload_entry_point(
        contents=entry_point_script_contents,
        node=node)

    return format_sbatch_allocation_request(
        args,
        entry_point_script=entry_point_script), entry_point_script


def run_sbatch(args: SbatchArguments,
               node: NodeInternal) -> Tuple[int, str]:
    """Runs sbatch on the given node. Returns the job id and the path
        to the entry point script.

        :param args: Arguments to use for allocation.

        :param node: Node to run sbatch on.

    """
    log = get_logger(__name__)

    request, entry_point_script_path = prepare_sbatch_allocation_request(
        args=args,
        config=node.config,
        node=node)
    log.debug("Allocation request: %s", request)
    output = node.run_impl(request,
                           install_keys=True)
    job_id = int(output.split(';')[0])

    return job_id, entry_point_script_path

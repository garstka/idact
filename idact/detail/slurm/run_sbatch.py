import shlex

from typing import Optional, Dict

from idact.core.nodes import Node
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


def format_sbatch_allocation_request(args: SbatchArguments) -> str:
    """Formats sbatch command from arguments.

        :param args: Arguments to append.
    """
    quoted_native = format_args(args=args.native_args)
    quoted = format_args(args=args.args)

    final = ("sbatch"
             " {quoted_native}"
             " {quoted}"
             " --tasks-per-node=1"  # One /bin/bash -c ... per node.
             " --parsable"
             " --output=/dev/null"
             " --wrap='srun /bin/bash -c"
             " \"trap : TERM INT; sleep infinity & wait\"'") \
        .format(quoted_native=quoted_native,
                quoted=quoted)
    return final


def run_sbatch(args: SbatchArguments,
               node: Node) -> int:
    """Runs sbatch on the given node. Returns the job id.

        :param args: Arguments to use for allocation.

        :param node: Node to run sbatch on.
    """

    request = format_sbatch_allocation_request(args=args)
    output = node.run(request)
    job_id = int(output.split(';')[0])

    return job_id

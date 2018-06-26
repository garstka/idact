import shlex

from idact.core.nodes import Node
from idact.detail.slurm.sbatch_arguments import SbatchArguments


def format_sbatch_allocation_request(args: SbatchArguments) -> str:
    """Formats sbatch command from arguments.

        :param args: Arguments to append.
    """
    argument_list = []
    for key, value in sorted(args.args.items()):
        argument_list.append(key)
        if value is not None:
            argument_list.append(value)

    quoted = ' '.join([shlex.quote(arg) for arg in argument_list])

    final = "sbatch {args}".format(args=quoted)
    final += (" --parsable"
              " --output=/dev/null"
              " --wrap='/bin/bash -c"
              " \"trap : TERM INT; sleep infinity & wait\"'")
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

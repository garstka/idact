import bitmath

from idact.core.nodes import Node

RES_MULTIPLIERS = {'m': 2 ** 10,
                   'g': 2 ** 20,
                   't': 2 ** 30,
                   'p': 2 ** 40}


def parse_top_res_format_to_kib(res: str) -> int:
    """Returns RES as KiB. Treats no suffix as KiB, then m=MiB, g=GiB,
        t=TiB, p=PiB.

        :param res: Res as string from top.

    """

    multiplier = RES_MULTIPLIERS.get(res[-1], None)
    if multiplier is None:
        return int(res)
    return int(float(res[:-1]) * multiplier)


def get_node_memory_usage(node: Node) -> bitmath.KiB:
    """Returns the sum of RES (Resident Memory Size) of all user processes
        on the node as reported by top."""
    # The commands below:
    # 1. Run top for one iteration.
    # 2. Skip the header and column names.
    # 3. Print only the column containing kibibytes used per process.
    # Values are not added up there, because awk does not support big integers.
    command = "top -b -n 1 -u $USER | awk 'NR>7 { print $6; }'"
    result = node.run(command)
    lines = result.splitlines()
    usage_by_process = map(parse_top_res_format_to_kib, lines)
    usage_total_int = sum(usage_by_process)
    usage_total_kibibytes = bitmath.KiB(usage_total_int)
    return usage_total_kibibytes

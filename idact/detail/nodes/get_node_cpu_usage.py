from idact.core.nodes import Node


def get_node_cpu_usage(node: Node) -> float:
    """Returns the sum of %CPU of all user processes as reported by top."""
    # The commands below:
    # 1. Run top for two iterations to get accurate CPU usage value.
    # 2. Skip output until 3 lines are encountered:
    #  - one new line between each header and process values,
    #  - one new line between iterations.
    # 3. Skip the next line containing column names.
    # 4. Calculate the sum of the column containing CPU usage.
    # 5. Print the sum.
    command = ("top -b -n 2 -d 1 -u $USER"
               " | sed '1,/^$/d;1,/^$/d;1,/^$/d'"
               " | awk 'NR>1 { sum += $9; } END { print sum; }'")
    top_result = node.run(command)
    usage_float = float(top_result)
    return usage_float

from typing import Optional, List, Tuple

from idact.detail.jupyter_app.app_allocation_parameters import \
    AppAllocationParameters


def override_parameters_if_possible(parameters: AppAllocationParameters,
                                    nodes: Optional[int],
                                    cores: Optional[int],
                                    memory_per_node: Optional[str],
                                    walltime: Optional[str],
                                    native_args: List[Tuple[str, str]]):
    """Overrides parameters with values from the command line, if they were
        provided.

        :param parameters: Parameters to override.

        :param nodes: Nodes from command line.

        :param cores: Cores from command line.

        :param memory_per_node: Memory from command line.

        :param walltime: Walltime from command line.

        :param native_args: Native args from command line.

    """
    if nodes is not None:
        parameters.nodes = nodes
    if cores is not None:
        parameters.cores = cores
    if memory_per_node is not None:
        parameters.memory_per_node = memory_per_node
    if walltime is not None:
        parameters.walltime = walltime
    if native_args:
        parameters.native_args = [[key for (key, _) in native_args],
                                  [value for (_, value) in native_args]]

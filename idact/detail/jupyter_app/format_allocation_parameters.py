from idact.detail.jupyter_app.app_allocation_parameters import \
    AppAllocationParameters


def format_allocation_parameters(parameters: AppAllocationParameters):
    """Formats allocation parameters for the user.

        :param parameters: Parameters to print.

    """
    result = "Allocation parameters:\n"
    result += "    Nodes: {}\n".format(parameters.nodes)
    result += "    Cores: {}\n".format(parameters.cores)
    result += "    Memory per node: {}\n".format(parameters.memory_per_node)
    result += "    Walltime: {}\n".format(parameters.walltime)
    if parameters.native_args[0] and parameters.native_args[1]:
        result += "    Native arguments:\n"
        for key, value in zip(parameters.native_args[0],
                              parameters.native_args[1]):
            if value == 'None':
                result += "      {}\n".format(key)
            else:
                result += "      {} -> {}\n".format(key, value)
    else:
        result += "    No native arguments.\n"

    return result

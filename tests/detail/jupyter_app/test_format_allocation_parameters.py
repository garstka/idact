from idact.detail.jupyter_app.app_allocation_parameters import \
    AppAllocationParameters
from idact.detail.jupyter_app.format_allocation_parameters import \
    format_allocation_parameters


def test_format_allocation_parameters():
    formatted = format_allocation_parameters(AppAllocationParameters(
        nodes=20,
        cores=10,
        memory_per_node='20 GiB',
        walltime='1-2:03:04',
        native_args=[['--arg1', '--arg2', '--arg3'],
                     ['value 1', 'None', '65']]))

    assert formatted == ("Allocation parameters:\n"
                         "    Nodes: 20\n"
                         "    Cores: 10\n"
                         "    Memory per node: 20 GiB\n"
                         "    Walltime: 1-2:03:04\n"
                         "    Native arguments:\n"
                         "      --arg1 -> value 1\n"
                         "      --arg2\n"
                         "      --arg3 -> 65\n")


def test_format_allocation_parameters_no_native_args():
    formatted = format_allocation_parameters(AppAllocationParameters(
        nodes=20,
        cores=10,
        memory_per_node='20 GiB',
        walltime='1-2:03:04'))

    assert formatted == ("Allocation parameters:\n"
                         "    Nodes: 20\n"
                         "    Cores: 10\n"
                         "    Memory per node: 20 GiB\n"
                         "    Walltime: 1-2:03:04\n"
                         "    No native arguments.\n")

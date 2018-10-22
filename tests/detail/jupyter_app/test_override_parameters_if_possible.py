from idact.detail.jupyter_app.app_allocation_parameters import \
    AppAllocationParameters
from idact.detail.jupyter_app.override_parameters_if_possible import \
    override_parameters_if_possible


def get_parameters_for_test() -> AppAllocationParameters:
    return AppAllocationParameters(
        nodes=10,
        cores=20,
        memory_per_node='30GiB',
        walltime='0:40:00',
        native_args=[['--arg1'],
                     ['value1']])


def test_override_nodes():
    parameters = get_parameters_for_test()

    override_parameters_if_possible(parameters=parameters,
                                    nodes=15,
                                    cores=None,
                                    memory_per_node=None,
                                    walltime=None,
                                    native_args=[])

    assert parameters == AppAllocationParameters(
        nodes=15,
        cores=20,
        memory_per_node='30GiB',
        walltime='0:40:00',
        native_args=[['--arg1'],
                     ['value1']])


def test_override_native_args():
    parameters = get_parameters_for_test()

    override_parameters_if_possible(parameters=parameters,
                                    nodes=None,
                                    cores=None,
                                    memory_per_node=None,
                                    walltime=None,
                                    native_args=[('--arg1', 'value2'),
                                                 ('--arg2', 'value3'),
                                                 ('--arg3', 'value4')])

    assert parameters == AppAllocationParameters(
        nodes=10,
        cores=20,
        memory_per_node='30GiB',
        walltime='0:40:00',
        native_args=[['--arg1', '--arg2', '--arg3'],
                     ['value2', 'value3', 'value4']])


def test_override_all():
    parameters = get_parameters_for_test()

    override_parameters_if_possible(parameters=parameters,
                                    nodes=15,
                                    cores=25,
                                    memory_per_node='35GiB',
                                    walltime='0:45:00',
                                    native_args=[('--arg2', 'value2')])

    assert parameters == AppAllocationParameters(
        nodes=15,
        cores=25,
        memory_per_node='35GiB',
        walltime='0:45:00',
        native_args=[['--arg2'],
                     ['value2']])

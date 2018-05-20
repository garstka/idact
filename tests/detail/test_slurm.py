import pytest
from bitmath import GiB

from idact import Walltime
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.slurm.run_sbatch import format_sbatch_allocation_request
from idact.detail.slurm.sbatch_arguments import SbatchArguments


def test_sbatch_arguments_create():
    params = AllocationParameters(nodes=1,
                                  cores=2,
                                  memory_per_node=GiB(1),
                                  walltime=Walltime(minutes=10))

    sbatch_args = SbatchArguments(params=params)

    assert sbatch_args.args == {'--nodes': '1',
                                '--ntasks-per-node': '2',
                                '--mem': '1048576K',
                                '--time': '0-00:10:00'}


def test_sbatch_arguments_create_with_native():
    params = AllocationParameters(nodes=1,
                                  cores=2,
                                  memory_per_node=GiB(1),
                                  walltime=Walltime(minutes=10),
                                  native_args={'--arg1': 'def',
                                               '--arg2': None,
                                               '--mem': '8G'})

    sbatch_args = SbatchArguments(params=params)

    assert sbatch_args.args == {'--nodes': '1',
                                '--ntasks-per-node': '2',
                                '--mem': '8G',
                                '--time': '0-00:10:00',
                                '--arg1': 'def',
                                '--arg2': None}


def test_sbatch_arguments_missing_required():
    with pytest.raises(ValueError):
        SbatchArguments(params=AllocationParameters(nodes=1,
                                                    cores=2,
                                                    memory_per_node=GiB(1)))


def test_sbatch_arguments_unsupported_provided():
    params = AllocationParameters(nodes=1,
                                  cores=2,
                                  walltime=Walltime(minutes=10),
                                  memory_per_node=GiB(1))
    params.all['Provided Unsupported Param'] = 12
    with pytest.raises(ValueError):
        SbatchArguments(params=params)


def test_format_sbatch_allocation_request():
    params = AllocationParameters(nodes=1,
                                  cores=2,
                                  memory_per_node=GiB(1),
                                  walltime=Walltime(minutes=10),
                                  native_args={'--arg1': 'def; rm -rf /abc &&',
                                               '--arg2': None,
                                               '--arg3': 'a b c',
                                               '--arg4 ||': '3',
                                               'arg5': '3#',
                                               '--mem': '8G'})

    args = SbatchArguments(params=params)

    formatted = format_sbatch_allocation_request(args=args)
    assert formatted == ("sbatch"
                         " --arg1 'def; rm -rf /abc &&'"
                         " --arg2"
                         " --arg3 'a b c'"
                         " '--arg4 ||' 3"
                         " --mem 8G"
                         " --nodes 1"
                         " --ntasks-per-node 2"
                         " --time 0-00:10:00"
                         " arg5 '3#'"
                         " --parsable"
                         " --output=/dev/null"
                         " --wrap='/bin/bash -c"
                         " \"trap : TERM INT; sleep infinity & wait\"'")

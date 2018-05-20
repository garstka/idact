from bitmath import GiB

from idact import Walltime
from idact.detail.allocation.allocation_parameters import AllocationParameters


def test_allocation_parameters_create_empty():
    params = AllocationParameters()

    assert params.all == {'nodes': None,
                          'cores': None,
                          'memory_per_node': None,
                          'walltime': None}
    assert params.native_args == {}


def test_allocation_parameters_create():
    params = AllocationParameters(nodes=1,
                                  cores=2,
                                  memory_per_node=GiB(1),
                                  walltime=Walltime(minutes=10),
                                  native_args={'--abc': None,
                                               '--def': '80'})

    assert params.all == {'nodes': 1,
                          'cores': 2,
                          'memory_per_node': GiB(1),
                          'walltime': Walltime(minutes=10)}
    assert params.nodes == 1
    assert params.cores == 2
    assert params.memory_per_node == GiB(1)
    assert params.walltime == Walltime(minutes=10)
    assert params.native_args == {'--abc': None,
                                  '--def': '80'}

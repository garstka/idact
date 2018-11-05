import bitmath
import pytest

from idact.core.walltime import Walltime
from idact.detail.allocation.allocation_parameters import AllocationParameters


def test_serialize_deserialize():
    value = AllocationParameters(nodes=20,
                                 cores=10,
                                 memory_per_node=bitmath.GiB(20),
                                 walltime=Walltime(days=1,
                                                   hours=12,
                                                   minutes=5,
                                                   seconds=32),
                                 native_args={'--arg1': 'value 1',
                                              '--arg2': None,
                                              '--arg3': '65'})
    serialized = value.serialize()
    assert serialized == {'type': 'SerializableTypes.ALLOCATION_PARAMETERS',
                          'nodes': 20,
                          'cores': 10,
                          'memory_per_node': '20.0 GiB',
                          'walltime': '1-12:05:32',
                          'native_args': {'--arg1': 'value 1',
                                          '--arg2': None,
                                          '--arg3': '65'}}

    deserialized = AllocationParameters.deserialize(serialized=serialized)
    assert deserialized == value


def test_serialize_deserialize_empty():
    value = AllocationParameters()
    serialized = value.serialize()
    assert serialized == {'type': 'SerializableTypes.ALLOCATION_PARAMETERS',
                          'nodes': None,
                          'cores': None,
                          'memory_per_node': None,
                          'walltime': None,
                          'native_args': {}}

    deserialized = AllocationParameters.deserialize(serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    serialized = {'type': 'SerializableTypes.ALLOCATION_PARAMETERS2'}

    with pytest.raises(AssertionError):
        AllocationParameters.deserialize(serialized=serialized)


def test_missing_serialized_keys():
    serialized = {'type': 'SerializableTypes.ALLOCATION_PARAMETERS'}

    with pytest.raises(RuntimeError):
        AllocationParameters.deserialize(serialized=serialized)

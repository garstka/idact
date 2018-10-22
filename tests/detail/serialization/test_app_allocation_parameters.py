import pytest

from idact.detail.jupyter_app.app_allocation_parameters import \
    AppAllocationParameters


def test_serialize_deserialize():
    value = AppAllocationParameters(
        nodes=20,
        cores=10,
        memory_per_node='20 GiB',
        walltime='1-2:03:04',
        native_args=[['--arg1', '--arg2', '--arg3'],
                     ['value 1', 'None', '65']])
    serialized = value.serialize()
    assert serialized == {
        'type': 'SerializableTypes.APP_ALLOCATION_PARAMETERS',
        'nodes': 20,
        'cores': 10,
        'memory_per_node': '20 GiB',
        'walltime': '1-2:03:04',
        'native_args': [['--arg1', '--arg2', '--arg3'],
                        ['value 1', 'None', '65']]}

    deserialized = AppAllocationParameters.deserialize(serialized=serialized)
    assert deserialized == value


def test_serialize_deserialize_empty():
    value = AppAllocationParameters()
    serialized = value.serialize()
    assert serialized == {
        'type': 'SerializableTypes.APP_ALLOCATION_PARAMETERS',
        'nodes': 1,
        'cores': 1,
        'memory_per_node': '1GiB',
        'walltime': '0:10:00',
        'native_args': [[], []]}

    deserialized = AppAllocationParameters.deserialize(serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    serialized = {'type': 'SerializableTypes.APP_ALLOCATION_PARAMETERS2'}

    with pytest.raises(AssertionError):
        AppAllocationParameters.deserialize(serialized=serialized)


def test_missing_serialized_keys():
    serialized = {'type': 'SerializableTypes.APP_ALLOCATION_PARAMETERS'}

    deserialized = AppAllocationParameters.deserialize(serialized=serialized)

    assert deserialized == AppAllocationParameters()


def test_deserialize_empty_dict():
    serialized = {}

    deserialized = AppAllocationParameters.deserialize(serialized=serialized)

    assert deserialized == AppAllocationParameters()

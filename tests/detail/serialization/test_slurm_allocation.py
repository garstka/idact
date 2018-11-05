import pytest

from idact.core.auth import AuthMethod
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.slurm.slurm_allocation import SlurmAllocation


def get_data_for_test():
    config = ClusterConfigImpl(host='localhost1',
                               port=1,
                               user='user-1',
                               auth=AuthMethod.ASK)
    access_node = NodeImpl(config=config)
    nodes = [NodeImpl(config=config),
             NodeImpl(config=config)]
    return access_node, nodes


def test_serialize_deserialize():
    access_node, nodes = get_data_for_test()

    value = SlurmAllocation(job_id=111,
                            access_node=access_node,
                            nodes=nodes,
                            entry_point_script_path='/a/b/c',
                            parameters=AllocationParameters())

    serialized = value.serialize()
    assert serialized == {
        'type': 'SerializableTypes.SLURM_ALLOCATION',
        'job_id': 111,
        'entry_point_script_path': '/a/b/c',
        'parameters': {'type': 'SerializableTypes.ALLOCATION_PARAMETERS',
                       'nodes': None,
                       'cores': None,
                       'memory_per_node': None,
                       'walltime': None,
                       'native_args': {}},
        'done_waiting': False}

    deserialized = SlurmAllocation.deserialize(access_node=access_node,
                                               nodes=nodes,
                                               serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    access_node, nodes = get_data_for_test()

    serialized = {'type': 'SerializableTypes.SLURM_ALLOCATION2'}

    with pytest.raises(AssertionError):
        SlurmAllocation.deserialize(access_node=access_node,
                                    nodes=nodes,
                                    serialized=serialized)


def test_missing_serialized_keys():
    access_node, nodes = get_data_for_test()

    serialized = {'type': 'SerializableTypes.SLURM_ALLOCATION'}

    with pytest.raises(RuntimeError):
        SlurmAllocation.deserialize(access_node=access_node,
                                    nodes=nodes,
                                    serialized=serialized)

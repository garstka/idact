import pytest

from idact.core.auth import AuthMethod
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.nodes_impl import NodesImpl
from idact.detail.slurm.slurm_allocation import SlurmAllocation


def get_data_for_test():
    config = ClusterConfigImpl(host='localhost1',
                               port=1,
                               user='user-1',
                               auth=AuthMethod.ASK)
    access_node = NodeImpl(config=config)

    return config, access_node


def test_serialize_deserialize():
    config, access_node = get_data_for_test()
    nodes = [NodeImpl(config=config),
             NodeImpl(config=config)]
    uuid = '1111'
    value = NodesImpl(nodes=nodes,
                      allocation=SlurmAllocation(
                          job_id=1,
                          access_node=access_node,
                          nodes=nodes,
                          entry_point_script_path='a',
                          parameters=AllocationParameters()),
                      uuid=uuid)

    serialized = value.serialize()
    assert serialized == {
        'type': 'SerializableTypes.NODES_IMPL',
        'nodes': [{'type': 'SerializableTypes.NODE_IMPL',
                   'host': None,
                   'port': None,
                   'cores': None,
                   'memory': None,
                   'allocated_until': None},
                  {'type': 'SerializableTypes.NODE_IMPL',
                   'host': None,
                   'port': None,
                   'cores': None,
                   'memory': None,
                   'allocated_until': None}],
        'allocation': {
            'type': 'SerializableTypes.SLURM_ALLOCATION',
            'job_id': 1,
            'entry_point_script_path': 'a',
            'parameters': {'type': 'SerializableTypes.ALLOCATION_PARAMETERS',
                           'nodes': None,
                           'cores': None,
                           'memory_per_node': None,
                           'walltime': None,
                           'native_args': {}},
            'done_waiting': False}}

    deserialized = NodesImpl.deserialize(config=config,
                                         access_node=access_node,
                                         serialized=serialized,
                                         uuid=uuid)
    assert deserialized == value


def test_invalid_serialized_type():
    config, access_node = get_data_for_test()

    serialized = {'type': 'SerializableTypes.NODES_IMPL2'}

    with pytest.raises(AssertionError):
        NodesImpl.deserialize(config=config,
                              access_node=access_node,
                              serialized=serialized,
                              uuid='1111')


def test_missing_serialized_keys():
    config, access_node = get_data_for_test()

    serialized = {'type': 'SerializableTypes.NODES_IMPL'}

    with pytest.raises(RuntimeError):
        NodesImpl.deserialize(config=config,
                              access_node=access_node,
                              uuid='1111',
                              serialized=serialized)

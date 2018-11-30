import pytest

from idact import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment.deserialize_generic_deployment import \
    deserialize_generic_deployment
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.nodes.node_impl import NodeImpl


def get_config_for_test():
    return ClusterConfigImpl(host='localhost1',
                             port=1,
                             user='user-1',
                             auth=AuthMethod.ASK)


def test_serialize_deserialize():
    config = get_config_for_test()
    value = GenericDeployment(node=NodeImpl(config=config),
                              pid=1,
                              runtime_dir='/dir')
    serialized = value.serialize()
    assert serialized == {'type': 'SerializableTypes.GENERIC_DEPLOYMENT',
                          'node': {'type': 'SerializableTypes.NODE_IMPL',
                                   'host': None,
                                   'port': None,
                                   'cores': None,
                                   'memory': None,
                                   'allocated_until': None},
                          'pid': 1,
                          'runtime_dir': '/dir'}

    deserialized = deserialize_generic_deployment(config=config,
                                                  serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    config = get_config_for_test()
    serialized = {'type': 'SerializableTypes.GENERIC_DEPLOYMENT2'}

    with pytest.raises(AssertionError):
        deserialize_generic_deployment(config=config,
                                       serialized=serialized)


def test_missing_serialized_keys():
    config = get_config_for_test()
    serialized = {'type': 'SerializableTypes.GENERIC_DEPLOYMENT'}

    with pytest.raises(RuntimeError):
        deserialize_generic_deployment(config=config,
                                       serialized=serialized)

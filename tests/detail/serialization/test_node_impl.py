import datetime

import bitmath
import dateutil.parser
import pytest

from idact.core.auth import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.nodes.node_impl import NodeImpl


def get_config_for_test():
    return ClusterConfigImpl(host='localhost1',
                             port=1,
                             user='user-1',
                             auth=AuthMethod.ASK)


def test_serialize_deserialize():
    config = get_config_for_test()

    value = NodeImpl(config=config)
    value.make_allocated(host='node1',
                         port=12323,
                         cores=30,
                         memory=bitmath.GiB(60),
                         allocated_until=(
                             datetime.datetime(2018, 11, 12, 13, 14).replace(
                                 tzinfo=dateutil.tz.tzutc())))

    serialized = value.serialize()
    assert serialized == {'type': 'SerializableTypes.NODE_IMPL',
                          'host': 'node1',
                          'port': 12323,
                          'cores': 30,
                          'memory': '60.0 GiB',
                          'allocated_until': '2018-11-12T13:14:00+00:00'}

    deserialized = NodeImpl.deserialize(config=config,
                                        serialized=serialized)
    assert deserialized == value


def test_serialize_deserialize_not_allocated():
    config = get_config_for_test()

    value = NodeImpl(config=config)

    serialized = value.serialize()
    assert serialized == {'type': 'SerializableTypes.NODE_IMPL',
                          'host': None,
                          'port': None,
                          'cores': None,
                          'memory': None,
                          'allocated_until': None}

    deserialized = NodeImpl.deserialize(config=config,
                                        serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    config = get_config_for_test()

    serialized = {'type': 'SerializableTypes.NODE_IMPL2'}

    with pytest.raises(AssertionError):
        NodeImpl.deserialize(config=config,
                             serialized=serialized)


def test_missing_serialized_keys():
    config = get_config_for_test()

    serialized = {'type': 'SerializableTypes.NODE_IMPL'}

    with pytest.raises(RuntimeError):
        NodeImpl.deserialize(config=config,
                             serialized=serialized)

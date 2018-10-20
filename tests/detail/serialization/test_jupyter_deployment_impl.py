import pytest

from idact.core.auth import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.jupyter.deserialize_jupyter_deployment_impl import \
    deserialize_jupyter_deployment_impl
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.detail.nodes.node_impl import NodeImpl
from tests.helpers.fake_tunnel import FakeTunnelAnyLocalPort


def get_data_for_test():
    config = ClusterConfigImpl(host='localhost1',
                               port=1,
                               user='user-1',
                               auth=AuthMethod.ASK)

    uuid = 'uuid1'
    return config, uuid


def test_serialize_deserialize():
    config, uuid = get_data_for_test()
    value = JupyterDeploymentImpl(
        deployment=GenericDeployment(
            node=NodeImpl(config=config),
            pid=111,
            output='out1',
            runtime_dir='/dir'),
        tunnel=FakeTunnelAnyLocalPort(there=1111),
        token='abcdefg',
        uuid=uuid)

    serialized = value.serialize()
    assert serialized == {
        'type': 'SerializableTypes.JUPYTER_DEPLOYMENT_IMPL',
        'deployment': {'type': 'SerializableTypes.GENERIC_DEPLOYMENT',
                       'node': {'type': 'SerializableTypes.NODE_IMPL',
                                'host': None,
                                'port': None,
                                'cores': None,
                                'memory': None,
                                'allocated_until': None},
                       'pid': 111,
                       'output': 'out1',
                       'runtime_dir': '/dir'},
        'tunnel_there': 1111,
        'token': 'abcdefg'}

    def fake_tunnel(_, there: int, here=None):
        assert here is None
        return FakeTunnelAnyLocalPort(there=there)

    saved_tunnel = NodeImpl.tunnel
    try:
        NodeImpl.tunnel = fake_tunnel
        deserialized = deserialize_jupyter_deployment_impl(
            config=config,
            uuid=uuid,
            serialized=serialized)
    finally:
        NodeImpl.tunnel = saved_tunnel

    assert deserialized == value


def test_invalid_serialized_type():
    config, uuid = get_data_for_test()

    serialized = {'type': 'SerializableTypes.JUPYTER_DEPLOYMENT_IMPL2'}

    with pytest.raises(AssertionError):
        deserialize_jupyter_deployment_impl(config=config,
                                            uuid=uuid,
                                            serialized=serialized)


def test_missing_serialized_keys():
    config, uuid = get_data_for_test()

    serialized = {'type': 'SerializableTypes.JUPYTER_DEPLOYMENT_IMPL'}

    with pytest.raises(RuntimeError):
        deserialize_jupyter_deployment_impl(config=config,
                                            uuid=uuid,
                                            serialized=serialized)

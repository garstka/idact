import pytest

from idact.core.auth import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.dask.dask_deployment_impl import DaskDeploymentImpl
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.nodes.node_impl import NodeImpl
from tests.helpers.fake_tunnel import FakeTunnel, use_fake_tunnel


def get_data_for_test():
    config = ClusterConfigImpl(host='localhost1',
                               port=1,
                               user='user-1',
                               auth=AuthMethod.ASK)

    uuid = 'uuid1'

    deployment = GenericDeployment(
        node=NodeImpl(config=config),
        pid=111,
        runtime_dir='/dir1')
    serialized_deployment = deployment.serialize()

    return config, uuid, deployment, serialized_deployment


def test_serialize_deserialize():
    config, uuid, deployment, serialized_deployment = get_data_for_test()
    value = DaskDeploymentImpl(
        scheduler=DaskSchedulerDeployment(
            deployment=deployment,
            tunnel=FakeTunnel(here=2222, there=1111),
            bokeh_tunnel=FakeTunnel(here=4444, there=3333),
            address='address1'),
        workers=[
            DaskWorkerDeployment(
                deployment=deployment,
                bokeh_tunnel=FakeTunnel(here=6666, there=5555)),
            DaskWorkerDeployment(
                deployment=deployment,
                bokeh_tunnel=FakeTunnel(here=8888, there=7777))],
        uuid=uuid)

    serialized = value.serialize()

    assert serialized == {
        'scheduler': {'address': 'address1',
                      'bokeh_tunnel_here': 4444,
                      'bokeh_tunnel_there': 3333,
                      'deployment': serialized_deployment,
                      'tunnel_here': 2222,
                      'tunnel_there': 1111,
                      'type': 'SerializableTypes.DASK_SCHEDULER_DEPLOYMENT'},
        'type': 'SerializableTypes.DASK_DEPLOYMENT_IMPL',
        'workers': [{'bokeh_tunnel_here': 6666,
                     'bokeh_tunnel_there': 5555,
                     'deployment': serialized_deployment,
                     'type': 'SerializableTypes.DASK_WORKER_DEPLOYMENT'},
                    {'bokeh_tunnel_here': 8888,
                     'bokeh_tunnel_there': 7777,
                     'deployment': serialized_deployment,
                     'type': 'SerializableTypes.DASK_WORKER_DEPLOYMENT'}]}

    with use_fake_tunnel():
        deserialized = DaskDeploymentImpl.deserialize(
            config=config,
            uuid=uuid,
            serialized=serialized)

    assert deserialized == value


def test_invalid_serialized_type():
    config, uuid, _, _ = get_data_for_test()

    serialized = {'type': 'SerializableTypes.DASK_DEPLOYMENT_IMPL2'}

    with pytest.raises(AssertionError):
        DaskDeploymentImpl.deserialize(config=config,
                                       uuid=uuid,
                                       serialized=serialized)


def test_missing_serialized_keys():
    config, uuid, _, _ = get_data_for_test()

    serialized = {'type': 'SerializableTypes.DASK_DEPLOYMENT_IMPL'}

    with pytest.raises(RuntimeError):
        DaskDeploymentImpl.deserialize(config=config,
                                       uuid=uuid,
                                       serialized=serialized)

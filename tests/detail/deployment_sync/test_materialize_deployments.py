import datetime

import bitmath

from idact import AuthMethod, ClusterConfig
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.deployment_sync.materialize_deployments import \
    materialize_deployments
from idact.detail.deployment_sync.synchronized_deployments_impl import \
    SynchronizedDeploymentsImpl
from idact.detail.helper.utc_now import utc_now
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.nodes_impl import NodesImpl
from idact.detail.slurm.slurm_allocation import SlurmAllocation


def get_common_data_for_test():
    config = ClusterConfigImpl(host='localhost1',
                               port=1,
                               user='user-1',
                               auth=AuthMethod.ASK)
    access_node = NodeImpl(config=config)
    return config, access_node


def get_expected_nodes_impl_for_test(config: ClusterConfig,
                                     access_node: NodeImpl,
                                     uuid: str,
                                     allocated_until: datetime.datetime):
    nodes = [NodeImpl(config=config)]
    nodes[0].make_allocated(host='h',
                            port=1,
                            cores=1,
                            memory=bitmath.GiB(1),
                            allocated_until=allocated_until)
    return NodesImpl(nodes=nodes,
                     allocation=SlurmAllocation(
                         job_id=111,
                         access_node=access_node,
                         nodes=nodes,
                         entry_point_script_path='a',
                         parameters=AllocationParameters()),
                     uuid=uuid)


# pylint: disable=bad-continuation
def get_deployment_definition_value_for_test(
    allocated_until: datetime.datetime) -> dict:  # noqa
    return {'type': 'SerializableTypes.NODES_IMPL',
            'nodes': [{'type': 'SerializableTypes.NODE_IMPL',
                       'host': 'h',
                       'port': 1,
                       'cores': 1,
                       'memory': '1.0 GiB',
                       'allocated_until': allocated_until.isoformat()}],
            'allocation': {
                'type': 'SerializableTypes.SLURM_ALLOCATION',
                'job_id': 111,
                'entry_point_script_path': 'a',
                'parameters': {
                    'type': 'SerializableTypes.ALLOCATION_PARAMETERS',
                    'nodes': None,
                    'cores': None,
                    'memory_per_node': None,
                    'walltime': None,
                    'native_args': {}},
                'done_waiting': False}}


# pylint: disable=bad-continuation
def get_deployment_definition_for_test(
    allocated_until: datetime.datetime) -> DeploymentDefinition:  # noqa
    return DeploymentDefinition(
        value=get_deployment_definition_value_for_test(
            allocated_until=allocated_until),
        expiration_date=allocated_until)


def test_materialize_nodes_deployments():
    """Expired deployment is not discarded.
        Deployments are ordered by expiration date."""
    config, access_node = get_common_data_for_test()
    base = utc_now()

    time_111 = base - datetime.timedelta(hours=10)
    time_222 = base + datetime.timedelta(hours=20)
    time_333 = base + datetime.timedelta(hours=10)

    print(str(get_expected_nodes_impl_for_test(config=config,
                                               access_node=access_node,
                                               uuid='111',
                                               allocated_until=time_111)))
    expected_synchronized_deployments = SynchronizedDeploymentsImpl(
        nodes=[get_expected_nodes_impl_for_test(config=config,
                                                access_node=access_node,
                                                uuid='111',
                                                allocated_until=time_111),
               get_expected_nodes_impl_for_test(config=config,
                                                access_node=access_node,
                                                uuid='333',
                                                allocated_until=time_333),
               get_expected_nodes_impl_for_test(config=config,
                                                access_node=access_node,
                                                uuid='222',
                                                allocated_until=time_222)])

    deployment_definitions = DeploymentDefinitions(
        nodes={
            '111': get_deployment_definition_for_test(
                allocated_until=time_111),
            '222': get_deployment_definition_for_test(
                allocated_until=time_222),
            '333': get_deployment_definition_for_test(
                allocated_until=time_333)
        })

    actual_synchronized_deployments = materialize_deployments(
        config=config,
        access_node=access_node,
        deployments=deployment_definitions)

    assert expected_synchronized_deployments.nodes == (
        actual_synchronized_deployments.nodes)


def test_materialize_nodes_deployments_different_expiration_dates():
    config, access_node = get_common_data_for_test()
    base = utc_now()

    time_111 = base + datetime.timedelta(hours=30)
    time_222 = base + datetime.timedelta(hours=10)
    time_333 = base + datetime.timedelta(hours=20)

    expected_synchronized_deployments = SynchronizedDeploymentsImpl(
        nodes=[get_expected_nodes_impl_for_test(config=config,
                                                access_node=access_node,
                                                uuid='222',
                                                allocated_until=time_222),
               get_expected_nodes_impl_for_test(config=config,
                                                access_node=access_node,
                                                uuid='333',
                                                allocated_until=time_333),
               get_expected_nodes_impl_for_test(config=config,
                                                access_node=access_node,
                                                uuid='111',
                                                allocated_until=time_111)])

    deployment_definitions = DeploymentDefinitions(
        nodes={
            '111': get_deployment_definition_for_test(
                allocated_until=time_111),
            '222': get_deployment_definition_for_test(
                allocated_until=time_222),
            '333': get_deployment_definition_for_test(
                allocated_until=time_333)
        })

    actual_synchronized_deployments = materialize_deployments(
        config=config,
        access_node=access_node,
        deployments=deployment_definitions)

    assert expected_synchronized_deployments == actual_synchronized_deployments

    assert str(expected_synchronized_deployments) == (
        repr(expected_synchronized_deployments))

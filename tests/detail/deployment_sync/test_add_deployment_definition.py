from idact import AuthMethod
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment_sync.add_deployment_definition import \
    add_deployment_definition
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.nodes_impl import NodesImpl
from idact.detail.slurm.slurm_allocation import SlurmAllocation


def get_deployment_for_test(uuid: str, job_id: int) -> NodesImpl:
    config = ClusterConfigImpl(host='localhost1',
                               port=1,
                               user='user-1',
                               auth=AuthMethod.ASK)
    access_node = NodeImpl(config=config)

    nodes = [NodeImpl(config=config),
             NodeImpl(config=config)]
    deployment = NodesImpl(nodes=nodes,
                           allocation=SlurmAllocation(
                               job_id=job_id,
                               access_node=access_node,
                               nodes=nodes,
                               entry_point_script_path='a',
                               parameters=AllocationParameters()),
                           uuid=uuid)
    return deployment


def test_definitions_can_be_added():
    deployments = DeploymentDefinitions()
    deployment1 = get_deployment_for_test(uuid='111', job_id=1)
    assert not deployments.nodes
    add_deployment_definition(deployments=deployments,
                              deployment=deployment1)
    assert len(deployments.nodes) == 1
    deployment2 = get_deployment_for_test(uuid='222', job_id=2)
    add_deployment_definition(deployments=deployments,
                              deployment=deployment2)
    assert len(deployments.nodes) == 2

    assert deployments.nodes['111'].value == deployment1.serialize()
    assert deployments.nodes['222'].value == deployment2.serialize()


def test_definition_with_the_same_uuid_is_replaced():
    deployments = DeploymentDefinitions()
    deployment_old = get_deployment_for_test(uuid='111', job_id=1)
    assert not deployments.nodes
    add_deployment_definition(deployments=deployments,
                              deployment=deployment_old)
    assert len(deployments.nodes) == 1
    assert deployments.nodes['111'].value == deployment_old.serialize()

    deployment_new = get_deployment_for_test(uuid='111', job_id=2)
    assert deployment_new.serialize() != deployment_old.serialize()

    add_deployment_definition(deployments=deployments,
                              deployment=deployment_new)
    assert len(deployments.nodes) == 1
    assert deployments.nodes['111'].value == deployment_new.serialize()

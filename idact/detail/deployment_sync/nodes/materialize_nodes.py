from idact.core.config import ClusterConfig
from idact.core.nodes import Nodes
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.nodes.nodes_impl import NodesImpl


def materialize_nodes(config: ClusterConfig,
                      access_node: NodeInternal,
                      uuid: str,
                      definition: DeploymentDefinition) -> Nodes:
    """Materializes the allocation deployment definition.

        :param config:      Cluster to materialize the nodes with.
        :param access_node: Access node of the cluster.
        :param uuid:        Unique deployment id.
        :param definition:  Deployment definition to materialize.

    """
    nodes = NodesImpl.deserialize(config=config,
                                  access_node=access_node,
                                  uuid=uuid,
                                  serialized=definition.value)
    return nodes

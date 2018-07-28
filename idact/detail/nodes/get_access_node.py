from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.nodes.node_impl import NodeImpl


def get_access_node(config: ClientClusterConfig) -> NodeImpl:
    """Returns the cluster access node, identified
       by :attr:`.ClientClusterConfig.host`.

       An access node is expected to be available without allocation.

       :param config: Client cluster config.

    """
    node = NodeImpl(config=config)
    node.make_allocated(host=config.host,
                        allocated_until=None)
    return node

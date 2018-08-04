from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl
from idact.detail.nodes.node_impl import NodeImpl


def get_access_node(config: ClusterConfigImpl) -> NodeImpl:
    """Returns the cluster access node, identified
        by :attr:`.ClusterConfig.host`.

        An access node is expected to be available without allocation.

        :param config: Client cluster config.

    """
    node = NodeImpl(config=config)
    node.make_allocated(host=config.host,
                        port=config.port,
                        allocated_until=None)
    return node

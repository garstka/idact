"""This module contains a function for getting the access node interface."""
from idact.core.config import ClusterConfig
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.node_internal import NodeInternal


def get_access_node(config: ClusterConfig) -> NodeInternal:
    """Returns the cluster access node, identified
        by :attr:`.ClusterConfig.host`.

        An access node is expected to be available without allocation.

        :param config: Client cluster config.

    """
    node = NodeImpl(config=config)
    node.make_allocated(host=config.host,
                        port=config.port,
                        cores=None,
                        memory=None,
                        allocated_until=None)
    return node

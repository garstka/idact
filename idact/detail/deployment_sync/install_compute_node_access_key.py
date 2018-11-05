from idact.detail.nodes.node_internal import NodeInternal


def install_compute_node_access_key(access_node: NodeInternal):
    """Adds the local key to authorized keys file for compute nodes,
        in case it was not added, which is a plausible scenario, when pulling
        deployments.

        :param access_node: Access node to install keys on.

    """
    access_node.run_impl("echo Testing connection...", install_keys=True)

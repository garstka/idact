from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl


def get_host_string(config: ClusterConfigImpl) -> str:
    """Returns the access node host string for Fabric.

        :param config: Cluster config.
    """
    return "{user}@{host}:{port}".format(user=config.user,
                                         host=config.host,
                                         port=config.port)

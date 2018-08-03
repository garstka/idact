from idact.core.auth import AuthMethod
from idact.detail.cluster_impl import ClusterImpl
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl


def test_cluster_create():
    client_cluster_config = ClusterConfigImpl(host='abc',
                                              port=22,
                                              user='user',
                                              auth=AuthMethod.ASK)
    ClusterImpl(config=client_cluster_config)

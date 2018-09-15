from idact import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.environment.environment_impl import EnvironmentImpl
from idact.detail.environment.merge_environments \
    import merge_cluster_configs, sanitize_cluster_config, \
    merge_common_clusters, sanitize_and_add_new_clusters, merge_environments


def test_merge_cluster_configs():
    cluster_1 = ClusterConfigImpl(host='localhost1',
                                  port=1,
                                  user='user-1',
                                  auth=AuthMethod.ASK,
                                  key='key1',
                                  install_key=False,
                                  disable_sshd=True,
                                  setup_actions=SetupActionsConfigImpl(
                                      jupyter=['command1'],
                                      dask=['command2']),
                                  scratch='/scratch1')

    cluster_2 = ClusterConfigImpl(host='localhost2',
                                  port=2,
                                  user='user-2',
                                  auth=AuthMethod.PUBLIC_KEY,
                                  key='key2',
                                  install_key=True,
                                  disable_sshd=False,
                                  setup_actions=SetupActionsConfigImpl(
                                      jupyter=['command3'],
                                      dask=['command4']),
                                  scratch='/scratch2')

    merged_1_2 = merge_cluster_configs(local=cluster_1,
                                       remote=cluster_2)

    merged_2_1 = merge_cluster_configs(local=cluster_2,
                                       remote=cluster_1)

    # Kept some fields from 1 after merge, replaced rest with 2.
    assert merged_1_2 == ClusterConfigImpl(
        host='localhost2',
        port=2,
        user='user-2',
        auth=AuthMethod.PUBLIC_KEY,
        key='key1',
        install_key=False,
        disable_sshd=False,
        setup_actions=SetupActionsConfigImpl(
            jupyter=['command3'],
            dask=['command4']),
        scratch='/scratch2')

    # Kept some fields from 2 after merge, replaced rest with 1.
    assert merged_2_1 == ClusterConfigImpl(
        host='localhost1',
        port=1,
        user='user-1',
        auth=AuthMethod.ASK,
        key='key2',
        install_key=True,
        disable_sshd=True,
        setup_actions=SetupActionsConfigImpl(
            jupyter=['command1'],
            dask=['command2']),
        scratch='/scratch1')

    # No changes.
    assert cluster_1 == ClusterConfigImpl(
        host='localhost1',
        port=1,
        user='user-1',
        auth=AuthMethod.ASK,
        key='key1',
        install_key=False,
        disable_sshd=True,
        setup_actions=SetupActionsConfigImpl(
            jupyter=['command1'],
            dask=['command2']),
        scratch='/scratch1')

    # No changes.
    assert cluster_2 == ClusterConfigImpl(
        host='localhost2',
        port=2,
        user='user-2',
        auth=AuthMethod.PUBLIC_KEY,
        key='key2',
        install_key=True,
        disable_sshd=False,
        setup_actions=SetupActionsConfigImpl(
            jupyter=['command3'],
            dask=['command4']),
        scratch='/scratch2')


def test_sanitize_cluster_config():
    cluster = ClusterConfigImpl(
        host='localhost1',
        port=1,
        user='user-1',
        auth=AuthMethod.ASK,
        key='key1',
        install_key=False,
        disable_sshd=True,
        setup_actions=SetupActionsConfigImpl(
            jupyter=['command1'],
            dask=['command2']),
        scratch='/scratch1')

    sanitized = sanitize_cluster_config(remote=cluster)

    # Cleared some fields.
    assert sanitized == ClusterConfigImpl(
        host='localhost1',
        port=1,
        user='user-1',
        auth=AuthMethod.ASK,
        key=None,
        install_key=True,
        disable_sshd=True,
        setup_actions=SetupActionsConfigImpl(
            jupyter=['command1'],
            dask=['command2']),
        scratch='/scratch1')


def test_merge_common_clusters():
    auth = AuthMethod.PUBLIC_KEY
    target_clusters = {'a': ClusterConfigImpl(host='localhost1',
                                              port=1,
                                              user='user-1',
                                              auth=auth),
                       'b': ClusterConfigImpl(host='localhost2',
                                              port=2,
                                              user='user-2',
                                              auth=auth),
                       'c': ClusterConfigImpl(host='localhost3',
                                              port=3,
                                              user='user-3',
                                              auth=auth)}

    remote_clusters = {'b': ClusterConfigImpl(host='localhost4',
                                              port=4,
                                              user='user-4',
                                              auth=auth),
                       'c': ClusterConfigImpl(host='localhost5',
                                              port=5,
                                              user='user-5',
                                              auth=auth),
                       'd': ClusterConfigImpl(host='localhost6',
                                              port=6,
                                              user='user-6',
                                              auth=auth)}

    merge_common_clusters(remote_clusters=remote_clusters,
                          target_clusters=target_clusters)

    # Merged common clusters with remote.
    assert target_clusters == {'a': ClusterConfigImpl(host='localhost1',
                                                      port=1,
                                                      user='user-1',
                                                      auth=auth),
                               'b': ClusterConfigImpl(host='localhost4',
                                                      port=4,
                                                      user='user-4',
                                                      auth=auth),
                               'c': ClusterConfigImpl(host='localhost5',
                                                      port=5,
                                                      user='user-5',
                                                      auth=auth)}

    # No changes.
    assert remote_clusters == {'b': ClusterConfigImpl(host='localhost4',
                                                      port=4,
                                                      user='user-4',
                                                      auth=auth),
                               'c': ClusterConfigImpl(host='localhost5',
                                                      port=5,
                                                      user='user-5',
                                                      auth=auth),
                               'd': ClusterConfigImpl(host='localhost6',
                                                      port=6,
                                                      user='user-6',
                                                      auth=auth)}


def test_sanitize_new_clusters():
    auth = AuthMethod.PUBLIC_KEY
    target_clusters = {'a': ClusterConfigImpl(host='localhost1',
                                              port=1,
                                              user='user-1',
                                              auth=auth),
                       'b': ClusterConfigImpl(host='localhost2',
                                              port=2,
                                              user='user-2',
                                              auth=auth),
                       'c': ClusterConfigImpl(host='localhost3',
                                              port=3,
                                              user='user-3',
                                              auth=auth)}

    remote_clusters = {'b': ClusterConfigImpl(host='localhost4',
                                              port=4,
                                              user='user-4',
                                              auth=auth),
                       'c': ClusterConfigImpl(host='localhost5',
                                              port=5,
                                              user='user-5',
                                              auth=auth),
                       'd': ClusterConfigImpl(host='localhost6',
                                              port=6,
                                              user='user-6',
                                              auth=auth)}

    sanitize_and_add_new_clusters(remote_clusters=remote_clusters,
                                  target_clusters=target_clusters)

    # Added new cluster.
    assert target_clusters == {'a': ClusterConfigImpl(host='localhost1',
                                                      port=1,
                                                      user='user-1',
                                                      auth=auth),
                               'b': ClusterConfigImpl(host='localhost2',
                                                      port=2,
                                                      user='user-2',
                                                      auth=auth),
                               'c': ClusterConfigImpl(host='localhost3',
                                                      port=3,
                                                      user='user-3',
                                                      auth=auth),
                               'd': ClusterConfigImpl(host='localhost6',
                                                      port=6,
                                                      user='user-6',
                                                      auth=auth)}

    # No changes.
    assert remote_clusters == {'b': ClusterConfigImpl(host='localhost4',
                                                      port=4,
                                                      user='user-4',
                                                      auth=auth),
                               'c': ClusterConfigImpl(host='localhost5',
                                                      port=5,
                                                      user='user-5',
                                                      auth=auth),
                               'd': ClusterConfigImpl(host='localhost6',
                                                      port=6,
                                                      user='user-6',
                                                      auth=auth)}


def test_merge_environments():
    auth = AuthMethod.PUBLIC_KEY
    environment_1 = EnvironmentImpl(
        config=ClientConfig(clusters={'a': ClusterConfigImpl(host='localhost1',
                                                             port=1,
                                                             user='user-1',
                                                             auth=auth,
                                                             key='key1'),
                                      'b': ClusterConfigImpl(host='localhost2',
                                                             port=2,
                                                             user='user-2',
                                                             auth=auth,
                                                             key='key1'),
                                      'c': ClusterConfigImpl(host='localhost3',
                                                             port=3,
                                                             user='user-3',
                                                             auth=auth)},
                            log_level=10))
    environment_2 = EnvironmentImpl(
        config=ClientConfig(clusters={'b': ClusterConfigImpl(host='localhost4',
                                                             port=4,
                                                             user='user-4',
                                                             auth=auth,
                                                             key='key2'),
                                      'c': ClusterConfigImpl(host='localhost5',
                                                             port=5,
                                                             user='user-5',
                                                             auth=auth),
                                      'd': ClusterConfigImpl(host='localhost6',
                                                             port=6,
                                                             user='user-6',
                                                             auth=auth,
                                                             key='key2')},
                            log_level=20))

    merged_1_2 = merge_environments(local=environment_1,
                                    remote=environment_2)

    # Kept some fields from 1 after merge, replaced rest with 2.
    # Sanitized some fields for new clusters from 2.
    assert merged_1_2 == EnvironmentImpl(
        config=ClientConfig(clusters={'a': ClusterConfigImpl(host='localhost1',
                                                             port=1,
                                                             user='user-1',
                                                             auth=auth,
                                                             key='key1'),
                                      'b': ClusterConfigImpl(host='localhost4',
                                                             port=4,
                                                             user='user-4',
                                                             auth=auth,
                                                             key='key1'),
                                      'c': ClusterConfigImpl(host='localhost5',
                                                             port=5,
                                                             user='user-5',
                                                             auth=auth),
                                      'd': ClusterConfigImpl(host='localhost6',
                                                             port=6,
                                                             user='user-6',
                                                             auth=auth,
                                                             key=None)},
                            log_level=10))

    merged_2_1 = merge_environments(local=environment_2,
                                    remote=environment_1)

    # Kept some fields from 2 after merge, replaced rest with 1.
    # Sanitized some fields for new clusters from 1.
    assert merged_2_1 == EnvironmentImpl(
        config=ClientConfig(clusters={'a': ClusterConfigImpl(host='localhost1',
                                                             port=1,
                                                             user='user-1',
                                                             auth=auth,
                                                             key=None),
                                      'b': ClusterConfigImpl(host='localhost2',
                                                             port=2,
                                                             user='user-2',
                                                             auth=auth,
                                                             key='key2'),
                                      'c': ClusterConfigImpl(host='localhost3',
                                                             port=3,
                                                             user='user-3',
                                                             auth=auth),
                                      'd': ClusterConfigImpl(host='localhost6',
                                                             port=6,
                                                             user='user-6',
                                                             auth=auth,
                                                             key='key2')},
                            log_level=20))

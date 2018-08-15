from logging import INFO, DEBUG

import pytest

from idact.core.auth import AuthMethod
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.config.client.client_config_serialize import \
    serialize_client_config_to_json, deserialize_client_config_from_json
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.log.logger_provider import LoggerProvider

VALID_CLIENT_CLUSTER_CONFIG = ClusterConfigImpl(host='abc',
                                                port=22,
                                                user='user',
                                                auth=AuthMethod.ASK)

VALID_CLIENT_CLUSTER_CONFIG_WITH_PUBLIC_KEY_AUTH = \
    ClusterConfigImpl(host='abc',
                      port=22,
                      user='user',
                      auth=AuthMethod.PUBLIC_KEY,
                      key='/home/user/.ssh/id_rsa',
                      install_key=False,
                      setup_actions=SetupActionsConfigImpl(jupyter=['echo a']))


def test_client_cluster_config_validation_is_used():
    with pytest.raises(ValueError):
        ClusterConfigImpl(host='',
                          port=22,
                          user='user',
                          auth=AuthMethod.ASK)
    with pytest.raises(ValueError):
        ClusterConfigImpl(host='abc',
                          port=-1,
                          user='user',
                          auth=AuthMethod.ASK)
    with pytest.raises(ValueError):
        ClusterConfigImpl(host='abc',
                          port=22,
                          user='',
                          auth=AuthMethod.ASK)
    with pytest.raises(ValueError):
        ClusterConfigImpl(host='abc',
                          port=22,
                          user='user',
                          auth=AuthMethod.PUBLIC_KEY,
                          key='')


def test_client_cluster_config_create():
    config = ClusterConfigImpl(host='abc',
                               port=22,
                               user='user',
                               auth=AuthMethod.ASK)
    assert config.host == 'abc'
    assert config.port == 22
    assert config.user == 'user'
    assert config.auth == AuthMethod.ASK
    assert config.key is None
    assert config.install_key
    assert not config.disable_sshd
    assert config.setup_actions.jupyter == []
    assert config.setup_actions.dask == []
    assert config.scratch == "$HOME"


def test_client_config_validation_is_used():
    cluster_cluster_config = VALID_CLIENT_CLUSTER_CONFIG
    with pytest.raises(ValueError):
        ClientConfig({' Illegal Cluster Name': cluster_cluster_config})


def test_client_config_create():
    cluster_cluster_config = VALID_CLIENT_CLUSTER_CONFIG
    print(cluster_cluster_config.__dict__)
    clusters = {'cluster1': cluster_cluster_config}
    client_config = ClientConfig(clusters=clusters)
    assert client_config.clusters is not clusters
    assert client_config.clusters['cluster1'] is cluster_cluster_config


def test_client_config_create_empty_and_add_cluster():
    client_config = ClientConfig()
    assert client_config.clusters == {}

    cluster_cluster_config = VALID_CLIENT_CLUSTER_CONFIG
    with pytest.raises(ValueError):
        client_config.add_cluster(' Illegal Cluster Name',
                                  cluster_cluster_config)
    assert client_config.clusters == {}

    client_config.add_cluster('cluster1', cluster_cluster_config)
    assert client_config.clusters['cluster1'] is cluster_cluster_config

    with pytest.raises(ValueError):
        client_config.add_cluster('cluster1',
                                  ClusterConfigImpl(host='another',
                                                    port=22,
                                                    user='user',
                                                    auth=AuthMethod.ASK))

    assert client_config.clusters['cluster1'] is cluster_cluster_config


def test_client_config_serialize():
    client_config = ClientConfig(clusters={
        'cluster1': VALID_CLIENT_CLUSTER_CONFIG
    }, log_level=INFO)
    expected_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'ASK',
                         'key': None,
                         'installKey': True,
                         'disableSshd': False,
                         'setupActions': {'jupyter': [],
                                          'dask': []},
                         'scratch': '$HOME'}
        },
        'logLevel': INFO
    }
    assert serialize_client_config_to_json(client_config) == expected_json


def test_client_config_deserialize():
    LoggerProvider().log_level = DEBUG
    input_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'ASK',
                         'key': None,
                         'installKey': True,
                         'disableSshd': False,
                         'setupActions': {'jupyter': [],
                                          'dask': []},
                         'scratch': '$HOME'}
        },
        'logLevel': DEBUG
    }
    client_config = ClientConfig(clusters={
        'cluster1': ClusterConfigImpl(host='abc',
                                      user='user',
                                      port=22,
                                      auth=AuthMethod.ASK)}, log_level=DEBUG)
    assert deserialize_client_config_from_json(input_json) == client_config


def test_client_config_serialize_public_key():
    client_config = ClientConfig(clusters={
        'cluster1': VALID_CLIENT_CLUSTER_CONFIG_WITH_PUBLIC_KEY_AUTH
    })
    expected_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'PUBLIC_KEY',
                         'key': '/home/user/.ssh/id_rsa',
                         'installKey': False,
                         'disableSshd': False,
                         'setupActions': {'jupyter': ['echo a'],
                                          'dask': []},
                         'scratch': '$HOME'}
        }, 'logLevel': INFO}
    assert serialize_client_config_to_json(client_config) == expected_json


def test_client_config_deserialize_public_key():
    input_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'PUBLIC_KEY',
                         'key': '/home/user/.ssh/id_rsa',
                         'installKey': False,
                         'disableSshd': False,
                         'setupActions': {'jupyter': ['echo a'],
                                          'dask': []},
                         'scratch': '$HOME'}
        },
        'logLevel': INFO
    }
    client_config = ClientConfig(clusters={
        'cluster1': VALID_CLIENT_CLUSTER_CONFIG_WITH_PUBLIC_KEY_AUTH})
    assert deserialize_client_config_from_json(input_json) == client_config


EXPECTED_DEFAULT_JSON = {
    'clusters': {
        'cluster1': {'host': 'abc',
                     'user': 'user',
                     'port': 22,
                     'auth': 'ASK',
                     'key': None,
                     'installKey': True,
                     'disableSshd': False,
                     'setupActions': {'jupyter': [],
                                      'dask': []},
                     'scratch': '$HOME'}
    },
    'logLevel': INFO
}


def test_client_config_fill_out_missing_fields():
    input_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'ASK'}
        },
        'logLevel': INFO
    }
    client_config = deserialize_client_config_from_json(input_json)

    assert serialize_client_config_to_json(client_config) == (
        EXPECTED_DEFAULT_JSON)


def test_client_config_fill_out_missing_fields_setup_actions():
    input_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'ASK',
                         'setupActions': {}}
        },
        'logLevel': INFO
    }
    client_config = deserialize_client_config_from_json(input_json)

    assert serialize_client_config_to_json(client_config) == (
        EXPECTED_DEFAULT_JSON)

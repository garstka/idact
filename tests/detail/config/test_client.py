from logging import INFO, DEBUG

import pytest

from idact.core.auth import AuthMethod
from idact.detail.config.client. \
    client_cluster_config import ClientClusterConfig
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.config.client.client_config_serialize import \
    serialize_client_config_to_json, deserialize_client_config_from_json

VALID_CLIENT_CLUSTER_CONFIG = ClientClusterConfig(host='abc',
                                                  port=22,
                                                  user='user',
                                                  auth=AuthMethod.ASK)

VALID_CLIENT_CLUSTER_CONFIG_WITH_PUBLIC_KEY_AUTH = \
    ClientClusterConfig(host='abc',
                        port=22,
                        user='user',
                        auth=AuthMethod.PUBLIC_KEY,
                        key='/home/user/.ssh/id_rsa',
                        install_key=False)


def test_client_cluster_config_validation_is_used():
    with pytest.raises(ValueError):
        ClientClusterConfig(host='',
                            port=22,
                            user='user',
                            auth=AuthMethod.ASK)
    with pytest.raises(ValueError):
        ClientClusterConfig(host='abc',
                            port=-1,
                            user='user',
                            auth=AuthMethod.ASK)
    with pytest.raises(ValueError):
        ClientClusterConfig(host='abc',
                            port=22,
                            user='',
                            auth=AuthMethod.ASK)
    with pytest.raises(ValueError):
        ClientClusterConfig(host='abc',
                            port=22,
                            user='user',
                            auth=AuthMethod.PUBLIC_KEY,
                            key='')


def test_client_cluster_config_create():
    config = ClientClusterConfig(host='abc',
                                 port=22,
                                 user='user',
                                 auth=AuthMethod.ASK)
    assert config.host == 'abc'
    assert config.port == 22
    assert config.user == 'user'
    assert config.auth == AuthMethod.ASK
    assert config.key is None
    assert config.install_key


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
                                  ClientClusterConfig(host='another',
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
                         'disableSshd': False}
        },
        'logLevel': INFO
    }
    assert serialize_client_config_to_json(client_config) == expected_json


def test_client_config_deserialize():
    input_json = {
        'clusters': {
            'cluster1': {'host': 'abc',
                         'user': 'user',
                         'port': 22,
                         'auth': 'ASK',
                         'key': None,
                         'installKey': True,
                         'disableSshd': False}
        },
        'logLevel': DEBUG
    }
    client_config = ClientConfig(clusters={
        'cluster1': ClientClusterConfig(host='abc',
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
                         'disableSshd': False}
        },
        'logLevel': INFO
    }
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
                         'disableSshd': False}
        },
        'logLevel': INFO
    }
    client_config = ClientConfig(clusters={
        'cluster1': VALID_CLIENT_CLUSTER_CONFIG_WITH_PUBLIC_KEY_AUTH})
    assert deserialize_client_config_from_json(input_json) == client_config

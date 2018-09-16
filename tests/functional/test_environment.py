import logging
import os
from contextlib import ExitStack
from pprint import pprint
from typing import List

import pytest

from idact import show_clusters, show_cluster, add_cluster, \
    AuthMethod, save_environment, load_environment, set_log_level, \
    ClusterConfig
from idact.core.remove_cluster import remove_cluster
from idact.detail.auth.set_password import set_password
from idact.detail.environment.environment_provider import EnvironmentProvider
from idact.detail.log.logger_provider import LoggerProvider
from tests.helpers.clear_environment import clear_environment
from tests.helpers.test_users import USER_2, get_test_user_password, USER_19, \
    USER_25, USER_26
from tests.helpers.testing_environment import TEST_CLUSTER


def test_environment():
    user = USER_2
    test_environment_file = './idact.test.conf'
    with ExitStack() as stack:
        stack.enter_context(clear_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        clusters = show_clusters()
        assert clusters == {}

        cluster = add_cluster(name=TEST_CLUSTER,
                              user=user,
                              host='localhost',
                              port=os.environ.get('SLURM_PORT', 2222))

        clusters = show_clusters()
        assert show_cluster(name=TEST_CLUSTER) is cluster
        assert len(show_clusters()) == 1
        assert clusters[TEST_CLUSTER] == cluster
        assert cluster.name == TEST_CLUSTER

        try:
            save_environment(path=test_environment_file)
            with clear_environment(user):
                assert show_clusters() == {}
                load_environment(path=test_environment_file)
                cluster2 = show_cluster(name=TEST_CLUSTER)
                assert cluster2 is not cluster
                assert cluster2 == cluster
        finally:
            os.remove(test_environment_file)


def check_config_is_default(config: ClusterConfig, user: str):
    assert config.host == 'localhost'
    assert config.port == 22
    assert config.user == user
    assert config.auth == AuthMethod.ASK
    assert config.key is None
    assert config.install_key
    assert not config.disable_sshd
    assert config.setup_actions.jupyter == []
    assert config.setup_actions.dask == []
    assert config.scratch == '$HOME'
    assert config.port_info_retries == 5
    assert LoggerProvider().log_level == logging.DEBUG


def check_config_is_modified(config: ClusterConfig):
    assert config.host == 'localhost2'
    assert config.port == 2222
    assert config.user == 'other'
    assert config.auth == AuthMethod.PUBLIC_KEY
    assert config.key == './fake-key'
    assert config.install_key is False
    assert config.disable_sshd
    assert config.setup_actions.jupyter == ['abc']
    assert config.setup_actions.dask == ['abc', 'def']
    assert config.scratch == '$HOME2'
    assert config.port_info_retries == 10
    assert LoggerProvider().log_level == logging.INFO


def get_default_config_contents(user: str) -> List[str]:
    return ['{',
            '    "clusters": {',
            '        "test": {',
            '            "auth": "ASK",',
            '            "disableSshd": false,',
            '            "host": "localhost",',
            '            "installKey": true,',
            '            "key": null,',
            '            "port": 22,',
            '            "portInfoRetries": 5,',
            '            "scratch": "$HOME",',
            '            "setupActions": {',
            '                "dask": [],',
            '                "jupyter": []',
            '            },',
            '            "user": "' + user + '"',
            '        }',
            '    },',
            '    "logLevel": 10',
            '}']


def test_environment_create_modify_save_load():
    user = USER_19
    test_environment_file = './idact.test.conf'
    test_environment_file2 = './idact.test2.conf'
    with ExitStack() as stack:
        stack.enter_context(clear_environment(user))

        assert show_clusters() == {}

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host='localhost')

        config = show_cluster(TEST_CLUSTER).config
        check_config_is_default(config=config, user=user)
        try:
            save_environment(path=test_environment_file)
            with open(test_environment_file, 'r') as test_file:
                contents = test_file.read().splitlines()

            pprint(contents)
            assert contents == get_default_config_contents(user=user)

            config = show_cluster(TEST_CLUSTER).config
            config.host = 'localhost2'
            config.port = 2222
            config.user = 'other'
            config.auth = AuthMethod.PUBLIC_KEY
            config.key = './fake-key'
            config.install_key = False
            config.disable_sshd = True
            config.setup_actions.jupyter = ['abc']
            config.setup_actions.dask = ['abc', 'def']
            config.scratch = '$HOME2'
            config.port_info_retries = 10
            set_log_level(logging.INFO)

            check_config_is_modified(config=config)

            save_environment(path=test_environment_file2)
            with open(test_environment_file2, 'r') as test_file:
                contents = test_file.read().splitlines()

            pprint(contents)
            assert contents == ['{',
                                '    "clusters": {',
                                '        "test": {',
                                '            "auth": "PUBLIC_KEY",',
                                '            "disableSshd": true,',
                                '            "host": "localhost2",',
                                '            "installKey": false,',
                                '            "key": "./fake-key",',
                                '            "port": 2222,',
                                '            "portInfoRetries": 10,',
                                '            "scratch": "$HOME2",',
                                '            "setupActions": {',
                                '                "dask": [',
                                '                    "abc",',
                                '                    "def"',
                                '                ],',
                                '                "jupyter": [',
                                '                    "abc"',
                                '                ]',
                                '            },',
                                '            "user": "other"',
                                '        }',
                                '    },',
                                '    "logLevel": 20',
                                '}']

            load_environment(test_environment_file)

            config = show_cluster(TEST_CLUSTER).config
            check_config_is_default(config=config, user=user)

            load_environment(test_environment_file2)

            config = show_cluster(TEST_CLUSTER).config
            check_config_is_modified(config=config)

        finally:
            try:
                os.remove(test_environment_file)
            finally:
                os.remove(test_environment_file2)


def test_environment_missing_and_defaults():
    user = USER_25
    with ExitStack() as stack:
        stack.enter_context(clear_environment(user))

        EnvironmentProvider()._environment = None  # noqa, pylint: disable=protected-access,line-too-long

        assert show_clusters() == {}

        assert not os.path.isfile(os.environ['IDACT_CONFIG_PATH'])

        with pytest.raises(ValueError):
            load_environment()

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host='localhost')

        config = show_cluster(TEST_CLUSTER).config
        set_log_level(logging.DEBUG)
        check_config_is_default(config=config, user=user)
        try:
            save_environment()
            with open(os.environ['IDACT_CONFIG_PATH'], 'r') as test_file:
                contents = test_file.read().splitlines()

            pprint(contents)
            assert contents == get_default_config_contents(user=user)

        finally:
            os.remove(os.environ['IDACT_CONFIG_PATH'])


def test_environment_add_cluster_and_remove():
    user = USER_26
    with ExitStack() as stack:
        stack.enter_context(clear_environment(user))

        assert show_clusters() == {}

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host='localhost')

        add_cluster(name='fake cluster',
                    user=user,
                    host='localhost2')

        assert len(show_clusters()) == 2

        cluster = show_cluster('fake cluster')

        assert cluster.config.host == 'localhost2'

        remove_cluster('fake cluster')

        assert len(show_clusters()) == 1

        add_cluster(name='fake cluster',
                    user=user,
                    host='localhost3')

        cluster2 = show_cluster('fake cluster')

        assert cluster.config.host == 'localhost2'
        assert cluster2.config.host == 'localhost3'

        cluster3 = show_cluster(TEST_CLUSTER)

        assert cluster3.config.host == 'localhost'

        remove_cluster('fake cluster')
        remove_cluster(TEST_CLUSTER)

        assert show_clusters() == {}

        with pytest.raises(KeyError):
            remove_cluster('fake cluster')

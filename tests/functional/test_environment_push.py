from contextlib import ExitStack
from json import JSONDecodeError
from typing import Optional

import pytest

from idact import show_cluster, push_environment, AuthMethod, add_cluster, \
    show_clusters
from idact.detail.auth.set_password import set_password
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment_impl import EnvironmentImpl
from idact.detail.environment.environment_text_serialization import \
    serialize_environment, deserialize_environment
from idact.detail.helper.get_remote_file import get_file_from_node
from idact.detail.helper.put_remote_file import put_file_on_node
from idact.detail.nodes.node_internal import NodeInternal
from tests.functional.test_environment_pull import \
    BASHRC_CONTENTS_WITH_IDACT_CONFIG_PATH_SET
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.paramiko_connect import paramiko_connect
from tests.helpers.remove_remote_file import remove_remote_file
from tests.helpers.reset_environment import reset_environment
from tests.helpers.test_users import get_test_user_password, USER_32, \
    USER_34, USER_35, USER_36, USER_37, USER_38, USER_4
from tests.helpers.testing_environment import TEST_CLUSTER, get_testing_host, \
    get_testing_port


def test_cannot_merge_push_environment_when_invalid_format_on_cluster():
    user = USER_32
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        node = cluster.get_access_node()
        node.run("echo abc > ~/idact-bad-config")
        with pytest.raises(JSONDecodeError):
            push_environment(cluster=cluster, path="~/idact-bad-config")


def check_able_to_merge_push_environment(user: str,
                                         remote_environment_upload_path: str,
                                         remote_environment_push_path:
                                         Optional[str]):
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(remove_remote_file(
            user=user,
            path=remote_environment_upload_path))

        cluster = show_cluster(name=TEST_CLUSTER)
        cluster.config.key = None
        cluster.config.install_key = False

        assert len(show_clusters()) == 1
        node = cluster.get_access_node()
        assert isinstance(node, NodeInternal)

        # Upload an environment to be merged on push.
        initial_remote_environment = EnvironmentImpl(
            config=ClientConfig(
                clusters={TEST_CLUSTER: ClusterConfigImpl(
                    host=get_testing_host(),
                    port=123,
                    user=user,
                    auth=AuthMethod.ASK,
                    key='key_remote',
                    install_key=True)}))

        initial_remote_environment_serialized = serialize_environment(
            environment=initial_remote_environment)

        put_file_on_node(node=node,
                         remote_path=remote_environment_upload_path,
                         contents=initial_remote_environment_serialized)

        # Modify current environment.
        fake_cluster = 'fake cluster'
        add_cluster(name=fake_cluster,
                    host='fakehost',
                    port=2,
                    user=user,
                    auth=AuthMethod.ASK,
                    key='key_local',
                    install_key=False)

        # Push with merge.
        push_environment(cluster=cluster,
                         path=remote_environment_push_path)

        remote_environment_after_push_serialized = \
            get_file_from_node(node=node,
                               remote_path=remote_environment_upload_path)

        remote_environment_after_push = deserialize_environment(
            text=remote_environment_after_push_serialized)

        # Remote key was kept unchanged.
        remote_clusters = remote_environment_after_push.config.clusters
        assert len(remote_clusters) == 2
        assert remote_clusters[TEST_CLUSTER] == ClusterConfigImpl(
            host=get_testing_host(),
            port=get_testing_port(),
            user=user,
            auth=AuthMethod.ASK,
            key='key_remote',
            install_key=True)

        # New cluster was sanitized
        assert remote_clusters[fake_cluster] == ClusterConfigImpl(
            host='fakehost',
            port=2,
            user=user,
            auth=AuthMethod.ASK,
            key=None,
            install_key=True)


def test_push_environment_to_default_location_with_merge():
    user = USER_34
    remote_environment_upload_path = '~/.idact.conf'
    remote_environment_push_path = None
    check_able_to_merge_push_environment(
        user=user,
        remote_environment_upload_path=remote_environment_upload_path,
        remote_environment_push_path=remote_environment_push_path)


def test_push_environment_to_custom_location_with_merge():
    user = USER_35
    remote_environment_upload_path = '~/.idact.conf-dev'
    remote_environment_push_path = remote_environment_upload_path
    check_able_to_merge_push_environment(
        user=user,
        remote_environment_upload_path=remote_environment_upload_path,
        remote_environment_push_path=remote_environment_push_path)


def test_push_environment_to_location_in_env_var_with_merge():
    user = USER_36
    with paramiko_connect(user) as ssh:
        ssh.exec_command("echo '{bashrc_contents}' > ~/.bashrc".format(
            bashrc_contents=BASHRC_CONTENTS_WITH_IDACT_CONFIG_PATH_SET))

    remote_environment_upload_path = '~/.idact-custom-config'
    remote_environment_push_path = None
    check_able_to_merge_push_environment(
        user=user,
        remote_environment_upload_path=remote_environment_upload_path,
        remote_environment_push_path=remote_environment_push_path)


def check_able_to_push_new_environment(user: str,
                                       remote_environment_expected_path: str,
                                       remote_environment_push_path: Optional[
                                           str]):
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(remove_remote_file(
            user=user,
            path=remote_environment_expected_path))

        cluster = show_cluster(name=TEST_CLUSTER)
        cluster.config.key = None
        cluster.config.install_key = False

        assert len(show_clusters()) == 1
        node = cluster.get_access_node()
        assert isinstance(node, NodeInternal)

        # Modify current environment.
        fake_cluster = 'fake cluster'
        add_cluster(name=fake_cluster,
                    host='fakehost',
                    port=2,
                    user=user,
                    auth=AuthMethod.ASK,
                    key='key_local',
                    install_key=False)

        # Target file does not exist.
        with pytest.raises(RuntimeError):
            node.run("cat {}".format(remote_environment_expected_path))

        push_environment(cluster=cluster,
                         path=remote_environment_push_path)

        remote_environment_after_push_serialized = \
            get_file_from_node(node=node,
                               remote_path=remote_environment_expected_path)

        remote_environment_after_push = deserialize_environment(
            text=remote_environment_after_push_serialized)

        # Both clusters were sanitized.
        remote_clusters = remote_environment_after_push.config.clusters
        assert len(remote_clusters) == 2
        assert remote_clusters[TEST_CLUSTER] == ClusterConfigImpl(
            host=get_testing_host(),
            port=get_testing_port(),
            user=user,
            auth=AuthMethod.ASK,
            key=None,
            install_key=True)

        assert remote_clusters[fake_cluster] == ClusterConfigImpl(
            host='fakehost',
            port=2,
            user=user,
            auth=AuthMethod.ASK,
            key=None,
            install_key=True)


def test_push_new_environment_to_default_location():
    user = USER_37
    remote_environment_expected_path = '~/.idact.conf'
    remote_environment_push_path = None
    check_able_to_push_new_environment(
        user=user,
        remote_environment_expected_path=remote_environment_expected_path,
        remote_environment_push_path=remote_environment_push_path)


def test_push_new_environment_to_custom_location():
    user = USER_38
    remote_environment_expected_path = '~/.idact.conf-dev'
    remote_environment_push_path = remote_environment_expected_path
    check_able_to_push_new_environment(
        user=user,
        remote_environment_expected_path=remote_environment_expected_path,
        remote_environment_push_path=remote_environment_push_path)


def test_push_new_environment_to_location_in_env_var():
    user = USER_4
    with paramiko_connect(user) as ssh:
        ssh.exec_command("echo '{bashrc_contents}' > ~/.bashrc".format(
            bashrc_contents=BASHRC_CONTENTS_WITH_IDACT_CONFIG_PATH_SET))

    remote_environment_expected_path = '~/.idact-custom-config'
    remote_environment_push_path = None
    check_able_to_push_new_environment(
        user=user,
        remote_environment_expected_path=remote_environment_expected_path,
        remote_environment_push_path=remote_environment_push_path)

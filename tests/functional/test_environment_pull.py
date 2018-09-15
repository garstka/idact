from contextlib import ExitStack
from json import JSONDecodeError
from typing import Optional

import pytest

from idact import show_cluster, pull_environment, AuthMethod, show_clusters
from idact.detail.auth.set_password import set_password
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment_impl import EnvironmentImpl
from idact.detail.environment.environment_text_serialization import \
    serialize_environment
from idact.detail.helper.put_remote_file import put_file_on_node
from idact.detail.nodes.node_internal import NodeInternal
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.paramiko_connect import paramiko_connect
from tests.helpers.remove_remote_file import remove_remote_file
from tests.helpers.reset_environment import reset_environment
from tests.helpers.test_users import USER_27, get_test_user_password, \
    USER_28, USER_30, USER_31, USER_33
from tests.helpers.testing_environment import TEST_CLUSTER, get_testing_host, \
    get_testing_port

BASHRC_CONTENTS_WITH_IDACT_CONFIG_PATH_SET = (
    "if [ -f /etc/bashrc ];"
    " then . /etc/bashrc;"
    " fi;"
    " export IDACT_CONFIG_PATH=~/.idact-custom-config")


def test_cannot_pull_environment_when_missing_on_cluster():
    user = USER_27
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        with pytest.raises(RuntimeError):
            pull_environment(cluster=cluster)


def test_cannot_pull_environment_when_invalid_format_on_cluster():
    user = USER_33
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        node = cluster.get_access_node()
        node.run("echo abc > ~/idact-bad-config")
        with pytest.raises(JSONDecodeError):
            pull_environment(cluster=cluster, path="~/idact-bad-config")


def check_able_to_pull_environment(user: str,
                                   remote_environment_upload_path: str,
                                   remote_environment_pull_path: Optional[
                                       str]):
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

        fake_cluster = 'fake cluster'
        remote_environment = EnvironmentImpl(
            config=ClientConfig(
                clusters={
                    TEST_CLUSTER: ClusterConfigImpl(
                        host=get_testing_host(),
                        port=get_testing_port(),
                        user=user,
                        auth=AuthMethod.ASK,
                        key='key_remote',
                        install_key=True),
                    fake_cluster: ClusterConfigImpl(
                        host='fakehost',
                        port=2,
                        user=user,
                        auth=AuthMethod.ASK,
                        key='key_remote',
                        install_key=True)}))

        remote_environment_serialized = serialize_environment(
            environment=remote_environment)

        node = cluster.get_access_node()
        assert isinstance(node, NodeInternal)

        put_file_on_node(node=node,
                         remote_path=remote_environment_upload_path,
                         contents=remote_environment_serialized)

        pull_environment(cluster=cluster,
                         path=remote_environment_pull_path)

        assert len(show_clusters()) == 2

        # Local key was kept unchanged.
        assert show_cluster(TEST_CLUSTER).config == ClusterConfigImpl(
            host=get_testing_host(),
            port=get_testing_port(),
            user=user,
            auth=AuthMethod.ASK,
            key=None,
            install_key=False)

        # New cluster was sanitized
        assert show_cluster(fake_cluster).config == ClusterConfigImpl(
            host='fakehost',
            port=2,
            user=user,
            auth=AuthMethod.ASK,
            key=None,
            install_key=True)


def test_pull_environment_from_default_location():
    user = USER_28
    remote_environment_upload_path = '~/.idact.conf'
    remote_environment_pull_path = None
    check_able_to_pull_environment(
        user=user,
        remote_environment_upload_path=remote_environment_upload_path,
        remote_environment_pull_path=remote_environment_pull_path)


def test_pull_environment_from_custom_location():
    user = USER_30
    remote_environment_upload_path = '~/.idact.conf-dev'
    remote_environment_pull_path = remote_environment_upload_path
    check_able_to_pull_environment(
        user=user,
        remote_environment_upload_path=remote_environment_upload_path,
        remote_environment_pull_path=remote_environment_pull_path)


def test_pull_environment_from_location_in_env_var():
    user = USER_31
    with paramiko_connect(user) as ssh:
        ssh.exec_command("echo '{bashrc_contents}' > ~/.bashrc".format(
            bashrc_contents=BASHRC_CONTENTS_WITH_IDACT_CONFIG_PATH_SET))

    remote_environment_upload_path = '~/.idact-custom-config'
    remote_environment_pull_path = None
    check_able_to_pull_environment(
        user=user,
        remote_environment_upload_path=remote_environment_upload_path,
        remote_environment_pull_path=remote_environment_pull_path)

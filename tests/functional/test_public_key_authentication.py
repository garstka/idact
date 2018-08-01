import os
from contextlib import ExitStack

import pytest
from bitmath import MiB
from fabric.context_managers import settings

from idact import AuthMethod, add_cluster, show_cluster, Walltime
from idact.core.auth import KeyType
from idact.detail.auth.generate_key import generate_key
from idact.detail.auth.set_password import set_password
from tests.helpers.clear_environment import clear_environment
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment, \
    get_testing_host, get_testing_port
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_8, get_test_user_password, USER_9, \
    USER_10, USER_11, USER_14, USER_12
from tests.helpers.testing_environment import TEST_CLUSTER


def test_able_to_reach_nodes_from_access_node_without_password():
    """It should be possible to connect to compute nodes from the access node,
       even when using password-based authentication, because remote, shared
       public key is authorized after initial connection. Password is still
       used between the client and the access node."""
    user = USER_10
    with ExitStack() as stack:
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user=user,
                                              auth=AuthMethod.ASK))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(disable_pytest_stdin())
        cluster = show_cluster(TEST_CLUSTER)
        node = cluster.get_access_node()

        nodes = cluster.allocate_nodes(nodes=2,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        print(nodes)

        try:
            nodes.wait(timeout=10)

            assert nodes[0].run('whoami') == user

            # Remote key was installed, allowing access between nodes
            # without password.
            assert node.run("ssh c1"
                            " -o UserKnownHostsFile=/dev/null"
                            " -o StrictHostKeyChecking=no"
                            " -o LogLevel=ERROR"
                            " whoami", timeout=1) == user
        finally:
            nodes.cancel()


def get_public_key_value() -> str:
    keys = os.listdir(os.environ['IDACT_KEY_LOCATION'])
    assert len(keys) == 2
    public_keys = [i for i in keys if i.endswith('.pub')]
    assert len(public_keys) == 1
    public_key = public_keys[0]
    private_key = [i for i in keys if i != public_key][0]
    assert private_key + '.pub' == public_key
    with open(os.path.join(os.environ['IDACT_KEY_LOCATION'],
                           public_key)) as file:
        return file.read()


def check_remote_key_and_node_access(user: str):
    public_key_value = get_public_key_value()

    cluster = show_cluster(name=TEST_CLUSTER)
    node = cluster.get_access_node()
    with set_password(get_test_user_password(user)):
        assert node.run('whoami') == user
    assert node.run('whoami') == user

    node.run("grep '{public_key_value}' ~/.ssh/authorized_keys".format(
        public_key_value=public_key_value))

    nodes = cluster.allocate_nodes(nodes=2,
                                   cores=1,
                                   memory_per_node=MiB(100),
                                   walltime=Walltime(minutes=30))
    print(nodes)

    try:
        nodes.wait(timeout=10)

        # Access to node without password works.
        assert nodes[0].run('whoami') == user

        # Remote key was installed, allowing access between nodes
        # without password.
        assert node.run("ssh c1"
                        " -o UserKnownHostsFile=/dev/null"
                        " -o StrictHostKeyChecking=no"
                        " -o LogLevel=ERROR"
                        " whoami", timeout=1) == user

    finally:
        nodes.cancel()


def generate_missing_key_prompttest_generate_and_install_key_on_access_node():
    with ExitStack() as stack:
        user = USER_8
        stack.enter_context(clear_environment(user))
        stack.enter_context(set_up_key_location())
        stack.enter_context(disable_pytest_stdin())

        with pytest.raises(ValueError):  # No key provided.
            add_cluster(name=TEST_CLUSTER,
                        user=user,
                        host=get_testing_host(),
                        port=get_testing_port(),
                        auth=AuthMethod.PUBLIC_KEY,
                        key=None,
                        install_key=True)

        # Generate RSA key.
        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host=get_testing_host(),
                    port=get_testing_port(),
                    auth=AuthMethod.PUBLIC_KEY,
                    key=KeyType.RSA,
                    install_key=True)

        check_remote_key_and_node_access(user=user)


def test_generate_but_do_not_install_key_on_access_node():
    with ExitStack() as stack:
        user = USER_9
        stack.enter_context(clear_environment(user))
        stack.enter_context(set_up_key_location())

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host=get_testing_host(),
                    port=get_testing_port(),
                    auth=AuthMethod.PUBLIC_KEY,
                    key=KeyType.RSA,
                    install_key=False)

        get_public_key_value()

        cluster = show_cluster(name=TEST_CLUSTER)
        node = cluster.get_access_node()
        with set_password(get_test_user_password(user)):
            # Would need to install key manually.
            with pytest.raises(RuntimeError):
                node.run('whoami')


def test_install_already_generated_key_on_access_node():
    with ExitStack() as stack:
        user = USER_11
        stack.enter_context(clear_environment(user))
        stack.enter_context(set_up_key_location())
        stack.enter_context(disable_pytest_stdin())

        key = generate_key(host=get_testing_host(),
                           key_type=KeyType.RSA)

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host=get_testing_host(),
                    port=get_testing_port(),
                    auth=AuthMethod.PUBLIC_KEY,
                    key=key,
                    install_key=True)

        check_remote_key_and_node_access(user=user)


def test_generate_and_install_missing_key_on_access_node():
    with ExitStack() as stack:
        user = USER_12
        stack.enter_context(clear_environment(user))
        stack.enter_context(set_up_key_location())
        stack.enter_context(disable_pytest_stdin())

        missing_key = os.path.join(os.environ['IDACT_KEY_LOCATION'],
                                   'id_rsa_fake')

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host=get_testing_host(),
                    port=get_testing_port(),
                    auth=AuthMethod.PUBLIC_KEY,
                    key=missing_key,
                    install_key=True)

        cluster = show_cluster(TEST_CLUSTER)
        node = cluster.get_access_node()

        generate_missing_key_prompt = (
            "Generate new public/private key pair? [Y/n] ")

        with set_password(get_test_user_password(user)):
            with pytest.raises(IOError):  # Will prompt for input.
                node.run('whoami')

            # Key missing and user chose not to generate one.
            with settings(prompts={generate_missing_key_prompt: 'n'}):
                with pytest.raises(RuntimeError):
                    node.run('whoami')

            # Key missing, generated and installed.
            with settings(prompts={generate_missing_key_prompt: 'y'}):
                assert node.run('whoami') == user

        check_remote_key_and_node_access(user=user)


def test_generate_and_install_key_no_sshd():
    with ExitStack() as stack:
        user = USER_14
        stack.enter_context(clear_environment(user))
        stack.enter_context(set_up_key_location())
        stack.enter_context(disable_pytest_stdin())

        add_cluster(name=TEST_CLUSTER,
                    user=user,
                    host=get_testing_host(),
                    port=get_testing_port(),
                    auth=AuthMethod.PUBLIC_KEY,
                    key=KeyType.RSA,
                    install_key=True,
                    disable_sshd=True)

        check_remote_key_and_node_access(user=user)

import socket
from contextlib import ExitStack

import pytest
import requests
from bitmath import MiB

import idact.detail.nodes.node_impl
from idact import show_cluster, Walltime, Nodes, AuthMethod
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.retry import retry
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit
from idact.detail.tunnel.tunnel_internal import TunnelInternal

from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.join_on_exit import join_on_exit
from tests.helpers.reset_environment import reset_environment
from tests.helpers.run_dummy_server import start_dummy_server_thread
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_5, USER_13, \
    USER_53, USER_54
from tests.helpers.testing_environment import TEST_CLUSTER


def run_tunnel_test(user: str, nodes: Nodes):
    node = nodes[0]
    nodes.wait(timeout=10)
    assert nodes.running()
    with ExitStack() as stack:
        stack.enter_context(cancel_on_exit(nodes))
        there = 8000
        here = 2223
        server = start_dummy_server_thread(user=user, server_port=there)
        stack.enter_context(join_on_exit(server))

        tunnel = node.tunnel(there=there, here=here)
        stack.enter_context(close_tunnel_on_exit(tunnel))

        print(tunnel)
        assert str(tunnel) == repr(tunnel)

        assert tunnel.here == here
        assert tunnel.there == there

        def access_dummy_server():
            return requests.get("http://127.0.0.1:{local_port}".format(
                local_port=here))

        request = retry(access_dummy_server,
                        retries=3,
                        seconds_between_retries=2)
        assert "text/html" in request.headers['Content-type']

        ssh_tunnel = node.tunnel_ssh()
        stack.enter_context(close_tunnel_on_exit(ssh_tunnel))

        assert str(ssh_tunnel) == repr(ssh_tunnel)
        assert str(ssh_tunnel).startswith("ssh ")
        assert user in str(ssh_tunnel)
        assert str(ssh_tunnel.here) in str(ssh_tunnel)
        assert ssh_tunnel.there == node.port

    assert not nodes.running()
    with pytest.raises(RuntimeError):
        nodes.wait()
    with pytest.raises(RuntimeError):
        node.tunnel(there=there, here=here)


def test_node_tunnel():
    """Allocates a node and creates a tunnel."""
    user = USER_5
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        run_tunnel_test(user=user, nodes=nodes)


def test_node_tunnel_public_key():
    """Allocates a node and creates a tunnel, uses public key authentication.
    """
    user = USER_13
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user=user,
                                              auth=AuthMethod.PUBLIC_KEY))

        cluster = show_cluster(name=TEST_CLUSTER)

        with set_password(get_test_user_password(user)):
            nodes = cluster.allocate_nodes(nodes=1,
                                           cores=1,
                                           memory_per_node=MiB(100),
                                           walltime=Walltime(minutes=30))
        run_tunnel_test(user=user, nodes=nodes)


def test_node_tunnel_fall_back_when_local_port_taken():
    """Checks that a tunnel will fall back to a random port if local port is
        taken."""
    user = USER_53
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))

        node = nodes[0]
        nodes.wait(timeout=10)

        there = 8000
        here = 2223

        tunnel_1 = node.tunnel(there=there, here=here)
        stack.enter_context(close_tunnel_on_exit(tunnel_1))
        assert tunnel_1.here == here

        tunnel_2 = node.tunnel(there=there, here=here)
        stack.enter_context(close_tunnel_on_exit(tunnel_2))
        assert tunnel_2.here != here


def test_node_tunnel_fall_back_when_local_port_free_but_fails():
    """Checks that a tunnel will fall back to a random port if local port is
        is initially free, but tunnel cannot be created anyway (e.g. another
        process binds to it at the last moment)."""
    user = USER_54
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))

        node = nodes[0]
        nodes.wait(timeout=10)

        there = 8000
        here = 2223

        real_build_tunnel = idact.detail.nodes.node_impl.build_tunnel
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tries = [0]

        def fake_build_tunnel(*args, **kwargs) -> TunnelInternal:
            tries[0] += 1
            if tries[0] == 1:
                raise RuntimeError("Fake failure.")
            if tries[0] != 2:
                assert False

            return real_build_tunnel(*args, **kwargs)

        try:
            idact.detail.nodes.node_impl.build_tunnel = fake_build_tunnel
            tunnel = node.tunnel(there=there, here=here)
            stack.enter_context(close_tunnel_on_exit(tunnel))
            assert tries[0] == 2
            assert tunnel.here != here
        finally:
            idact.detail.nodes.node_impl.build_tunnel = real_build_tunnel
            sock.close()

from contextlib import ExitStack

import pytest
import requests
from bitmath import MiB

from idact import show_cluster, Walltime, Nodes, AuthMethod
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.retry import retry
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit

from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.run_dummy_server import start_dummy_server_thread
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_5, USER_13
from tests.helpers.testing_environment import TEST_CLUSTER


def run_tunnel_test(user: str, nodes: Nodes):
    node = nodes[0]
    server = None
    try:
        nodes.wait(timeout=10)
        assert nodes.running()
        with ExitStack() as stack:
            stack.enter_context(cancel_on_exit(nodes))
            there = 8000
            here = 2223
            server = start_dummy_server_thread(user=user, server_port=there)

            tunnel = node.tunnel(there=there, here=here)
            print(tunnel)
            assert str(tunnel) == repr(tunnel)

            stack.enter_context(close_tunnel_on_exit(tunnel))
            assert tunnel.here == here
            assert tunnel.there == there

            def access_dummy_server():
                return requests.get("http://127.0.0.1:{local_port}".format(
                    local_port=here))

            request = retry(access_dummy_server,
                            retries=3,
                            seconds_between_retries=2)
            assert "text/html" in request.headers['Content-type']
    finally:
        if server is not None:
            server.join()

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

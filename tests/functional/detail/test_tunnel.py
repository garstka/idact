from contextlib import ExitStack
from typing import List

import requests

from idact import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.tunnel.build_tunnel import build_tunnel
from idact.detail.tunnel.binding import Binding
from idact.detail.helper.retry import retry
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit
from tests.helpers.join_on_exit import join_on_exit

from tests.helpers.reset_environment import get_testing_host, get_testing_port
from tests.helpers.run_dummy_server import start_dummy_server_thread
from tests.helpers.test_users import USER_3, get_test_user_password


def run_tunnel_test_for_bindings(bindings: List[Binding]):
    """Runs a tunneling test for a binding sequence.

        Runs a Python server in a separate thread through ssh, then creates
        a multi-hop tunnel, and finally performs a HTTP request to the local
        address.

        :param bindings: Sequence of tunnel bindings.

    """
    user = USER_3
    config = ClusterConfigImpl(host=get_testing_host(),
                               port=get_testing_port(),
                               user=user,
                               auth=AuthMethod.ASK)

    local_port = bindings[0].port
    server_port = bindings[-1].port

    with ExitStack() as stack:
        tunnel = build_tunnel(config=config,
                              bindings=bindings,
                              ssh_password=get_test_user_password(user))
        stack.enter_context(close_tunnel_on_exit(tunnel))

        server = start_dummy_server_thread(user=user,
                                           server_port=server_port)
        stack.enter_context(join_on_exit(server))

        assert tunnel.here == local_port
        assert tunnel.there == server_port

        def access_dummy_server():
            return requests.get("http://127.0.0.1:{local_port}".format(
                local_port=local_port))

        request = retry(access_dummy_server,
                        retries=3,
                        seconds_between_retries=2)
        assert "text/html" in request.headers['Content-type']


def test_tunnel_single_hop():
    bindings = [Binding("", 2223),
                Binding("127.0.0.1", 8000)]
    run_tunnel_test_for_bindings(bindings)


def test_tunnel_two_hops():
    bindings = [Binding("", 2223),
                Binding("127.0.0.1", 22),
                Binding("127.0.0.1", 8000)]
    run_tunnel_test_for_bindings(bindings)


def test_tunnel_multiple_hops():
    bindings = [Binding("", 2223),
                Binding("c1", 22),
                Binding("c2", 8022),
                Binding("c3", 8023),
                Binding("127.0.0.1", 8000)]
    run_tunnel_test_for_bindings(bindings)

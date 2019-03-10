from contextlib import ExitStack
from typing import List

import requests

from idact import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.helper.get_free_local_port import get_free_local_port
from idact.detail.helper.ports import PORT_3, PORT_1, PORT_2
from idact.detail.tunnel.build_tunnel import build_tunnel
from idact.detail.tunnel.binding import Binding
from idact.detail.helper.retry import retry
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit
from tests.helpers.join_on_exit import join_on_exit

from tests.helpers.reset_environment import get_testing_host, get_testing_port
from tests.helpers.run_dummy_server import start_dummy_server_thread
from tests.helpers.test_users import USER_3, get_test_user_password, USER_60, \
    USER_59
from tests.helpers.testing_environment import get_testing_process_count


def run_tunnel_test_for_bindings(user: str,
                                 bindings: List[Binding]):
    """Runs a tunneling test for a binding sequence.

        Runs a Python server in a separate thread through ssh, then creates
        a multi-hop tunnel, and finally performs a HTTP request to the local
        address.

        :param user: Test user.

        :param bindings: Sequence of tunnel bindings.

    """
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
                        retries=3 * get_testing_process_count(),
                        seconds_between_retries=2)
        assert "text/html" in request.headers['Content-type']


def test_tunnel_single_hop():
    user = USER_3
    bindings = [Binding("", get_free_local_port()),
                Binding("127.0.0.1", PORT_1)]
    run_tunnel_test_for_bindings(user=user, bindings=bindings)


def test_tunnel_two_hops():
    user = USER_59
    bindings = [Binding("", get_free_local_port()),
                Binding("127.0.0.1", 22),
                Binding("127.0.0.1", PORT_2)]
    run_tunnel_test_for_bindings(user=user, bindings=bindings)


def test_tunnel_multiple_hops():
    user = USER_60
    bindings = [Binding("", get_free_local_port()),
                Binding("c1", 22),
                Binding("c2", 8022),
                Binding("c3", 8023),
                Binding("127.0.0.1", PORT_3)]
    run_tunnel_test_for_bindings(user=user, bindings=bindings)

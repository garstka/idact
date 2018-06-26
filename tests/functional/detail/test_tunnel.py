from threading import Thread
from typing import List

import requests

from idact.detail.tunnel.build_tunnel import build_tunnel
from idact.detail.tunnel.binding import Binding
from tests.helpers.run_dummy_server import run_dummy_server
from tests.helpers.reset_environment import get_testing_host, get_testing_port
from tests.helpers.test_users import USER_3, get_test_user_password


def run_tunnel_test_for_bindings(bindings: List[Binding]):
    """Runs a tunneling test for a binding sequence.

       Runs a Python server in a separate thread through ssh, then creates
       a multi-hop tunnel, and finally performs a HTTP request to the local
       address.

        :param bindings: Sequence of tunnel bindings.
    """
    hostname = get_testing_host()
    port = get_testing_port()
    user = USER_3

    local_port = bindings[0].port
    server_port = bindings[-1].port
    timeout = 1

    tunnel = None
    thread = Thread(target=run_dummy_server, args=(server_port, timeout))
    try:
        tunnel = build_tunnel(bindings=bindings,
                              hostname=hostname,
                              port=port,
                              ssh_username=user,
                              ssh_password=get_test_user_password(user))
        thread.start()

        assert tunnel.here == local_port
        assert tunnel.there == server_port

        request = requests.get("http://127.0.0.1:{local_port}".format(
            local_port=local_port))
        assert "text/html" in request.headers['Content-type']
    finally:
        if tunnel is not None:
            tunnel.close()
        thread.join()


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

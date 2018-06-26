from contextlib import ExitStack
from threading import Thread

import pytest
import requests
from bitmath import MiB

from idact import show_cluster, Walltime
from idact.detail.auth.set_password import set_password
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment, TEST_CLUSTER
from tests.helpers.run_dummy_server import run_dummy_server
from tests.helpers.test_users import get_test_user_password, USER_5


def test_node_tunnel():
    """Allocates a node and creates a tunnel."""
    user = USER_5
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        node = nodes[0]
        server = None
        tunnel = None
        try:
            nodes.wait(timeout=10)
            assert nodes.running()

            there = 8000
            here = 2223
            timeout = 1
            server = Thread(target=run_dummy_server, args=(there, timeout))
            server.start()

            tunnel = node.tunnel(there=there, here=here)
            print(tunnel)

            assert tunnel.here == here
            assert tunnel.there == there

            request = requests.get("http://127.0.0.1:{local_port}".format(
                local_port=here))
            assert "text/html" in request.headers['Content-type']
        finally:
            if tunnel is not None:
                tunnel.close()
            if server is not None:
                server.join()
            nodes.cancel()

        assert not nodes.running()
        with pytest.raises(RuntimeError):
            nodes.wait()
        with pytest.raises(RuntimeError):
            node.tunnel(there=there, here=here)

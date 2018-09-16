from contextlib import ExitStack

from bitmath import MiB

from idact import show_cluster, Nodes
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit

from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.stress_cpu import start_stress_cpu, stop_stress_cpu
from tests.helpers.test_users import get_test_user_password, USER_40
from tests.helpers.testing_environment import TEST_CLUSTER


def run_tunnel_stress_test(user: str, nodes: Nodes):
    with ExitStack() as stack:
        node = nodes[0]
        nodes.wait(timeout=10)
        stack.enter_context(cancel_on_exit(nodes))

        there = 8000
        here = 2223

        try:
            for _ in range(5):
                start_stress_cpu(user=user, timeout=10)
            tunnel = node.tunnel(there=there, here=here)
            stack.enter_context(close_tunnel_on_exit(tunnel))
        finally:
            stop_stress_cpu(user=user)

        assert tunnel.here == here
        assert tunnel.there == there


def test_node_tunnel_stress():
    user = USER_40
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100))
        run_tunnel_stress_test(user=user, nodes=nodes)

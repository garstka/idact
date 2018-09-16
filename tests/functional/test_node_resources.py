from contextlib import ExitStack

import bitmath

from idact import show_cluster
from idact.core.node_resource_status import NodeResourceStatus
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.stress_cpu import start_stress_cpu, stop_stress_cpu
from tests.helpers.test_users import get_test_user_password, USER_39
from tests.helpers.testing_environment import TEST_CLUSTER


def check_resources_in_believable_range(resources: NodeResourceStatus):
    print(resources.cpu_usage)
    assert resources.cpu_usage > 0.0
    assert resources.cpu_usage <= 100.0
    print(resources.memory_usage)
    assert resources.memory_usage.value > 0.0
    assert resources.memory_usage.value < 2.0


def test_can_read_node_resources():
    user = USER_39
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)

        access_node = cluster.get_access_node()

        assert access_node.resources.cpu_cores is None
        assert access_node.resources.memory_total is None
        start_stress_cpu(user=user, timeout=10)
        try:
            check_resources_in_believable_range(access_node.resources)
        finally:
            stop_stress_cpu(user=user)

        nodes = cluster.allocate_nodes(cores=1,
                                       memory_per_node=bitmath.GiB(0.8))

        assert len(nodes) == 1
        node = nodes[0]

        stack.enter_context(cancel_on_exit(nodes))

        nodes.wait(timeout=10)
        assert nodes.running()

        assert node.resources.cpu_cores == 1
        assert node.resources.memory_total == bitmath.GiB(0.8)
        start_stress_cpu(user=user, timeout=10)
        try:
            check_resources_in_believable_range(access_node.resources)
        finally:
            stop_stress_cpu(user=user)

        assert node.run('whoami') == user

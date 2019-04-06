from contextlib import ExitStack

from bitmath import MiB

from idact import show_cluster
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.retry import retry
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_61, get_test_user_password
from tests.helpers.testing_environment import TEST_CLUSTER, SLURM_WAIT_TIMEOUT


def test_allocation_should_default_to_port_22_if_port_info_file_is_missing():
    user = USER_61
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)

        node = cluster.get_access_node()
        nodes = cluster.allocate_nodes(memory_per_node=MiB(100))
        stack.enter_context(cancel_on_exit(nodes))

        retry(lambda: node.run("rm ~/.idact/sshd_ports/alloc-*/*"),
              retries=SLURM_WAIT_TIMEOUT,
              seconds_between_retries=1)

        nodes.wait(timeout=SLURM_WAIT_TIMEOUT)

        assert nodes.running()
        assert nodes[0].port == 22

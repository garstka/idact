from contextlib import ExitStack

import bitmath
import pytest

from idact import show_cluster
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from tests.helpers.clear_deployment_sync_data import clear_deployment_sync_data
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_43, get_test_user_password, \
    USER_44, USER_45, USER_46
from tests.helpers.testing_environment import TEST_CLUSTER


def test_able_to_sync_nodes_before_and_after_wait():
    user = USER_43
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        nodes_2 = None
        nodes_3 = None
        try:
            deployments = cluster.pull_deployments()
            assert not deployments.nodes

            cluster.push_deployment(deployment=nodes)
            nodes = None
            deployments = cluster.pull_deployments()
            print(deployments)

            assert len(deployments.nodes) == 1
            nodes_2 = deployments.nodes[0]
            assert len(nodes_2) == 1
            nodes_2.wait(timeout=10)
            assert nodes_2.running()
            node_2 = nodes_2[0]

            cluster.push_deployment(deployment=nodes_2)
            nodes_2 = None
            deployments = cluster.pull_deployments()
            print(deployments)

            assert len(deployments.nodes) == 1
            nodes_3 = deployments.nodes[0]

            assert nodes_3.running()
            with pytest.raises(RuntimeError):
                nodes_3.wait()
            assert len(nodes_3) == 1
            node_3 = nodes_3[0]

            assert node_2.host == node_3.host
            assert node_2.port == node_3.port
            assert node_3.resources.cpu_cores == 1
            assert node_3.resources.memory_total == bitmath.GiB(1)
            print(node_3)

            assert node_3.run('whoami') == user
        finally:
            if nodes is not None:
                nodes.cancel()
            if nodes_2 is not None:
                nodes_2.cancel()
            if nodes_3 is not None:
                nodes_3.cancel()


def test_nodes_sync_does_not_work_when_waiting_twice():
    """Port info was already deleted, so waiting for the second time defaults
        to port 22."""
    user = USER_44
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        with cancel_on_exit(nodes):
            cluster.push_deployment(deployment=nodes)

            nodes.wait(timeout=10)
            assert nodes.running()
            node = nodes[0]
            assert node.port != 22

            deployments = cluster.pull_deployments()
            assert len(deployments.nodes) == 1
            nodes_2 = deployments.nodes[0]

            nodes_2.wait(timeout=10)
            assert nodes_2.running()
            node_2 = nodes_2[0]

            assert node_2.port == 22
            assert node_2.host == node.host


def test_cancelled_node_allocation_is_discarded_on_pull():
    user = USER_45
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        try:
            nodes.wait(timeout=10)
            assert nodes.running()

            cluster.push_deployment(deployment=nodes)

            deployments = cluster.pull_deployments()
            assert len(deployments.nodes) == 1
            assert deployments.nodes[0].running()
            nodes.cancel()
            nodes = None

            deployments = cluster.pull_deployments()
            assert not deployments.nodes
        finally:
            if nodes is not None:
                nodes.cancel()


def test_clear_deployments():
    user = USER_46
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)
        access_node = cluster.get_access_node()

        def check_deployments_file_exists():
            access_node.run("cat ~/.idact/.deployments")

        nodes = cluster.allocate_nodes()
        with cancel_on_exit(nodes):
            nodes.wait(timeout=10)
            assert nodes.running()

            with pytest.raises(RuntimeError):
                check_deployments_file_exists()

            cluster.push_deployment(deployment=nodes)

            check_deployments_file_exists()

            deployments = cluster.pull_deployments()
            assert len(deployments.nodes) == 1
            assert deployments.nodes[0].running()

            check_deployments_file_exists()

            cluster.clear_pushed_deployments()

            with pytest.raises(RuntimeError):
                check_deployments_file_exists()

            deployments = cluster.pull_deployments()
            assert not deployments.nodes

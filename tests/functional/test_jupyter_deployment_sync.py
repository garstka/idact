from contextlib import ExitStack

from idact import show_cluster
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from tests.helpers.check_local_http_connection import \
    check_local_http_connection
from tests.helpers.clear_deployment_sync_data import clear_deployment_sync_data
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_47, USER_48
from tests.helpers.testing_environment import TEST_CLUSTER


def test_able_to_sync_jupyter():
    user = USER_47
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        stack.enter_context(cancel_on_exit(nodes))
        node = nodes[0]
        nodes.wait(timeout=10)

        local_port = 2223
        jupyter = node.deploy_notebook(local_port=local_port)
        stack.enter_context(cancel_on_exit(jupyter))

        deployments = cluster.pull_deployments()
        assert not deployments.jupyter_deployments

        cluster.push_deployment(deployment=jupyter)
        deployments = cluster.pull_deployments()
        print(deployments)

        assert len(deployments.jupyter_deployments) == 1
        jupyter_2 = deployments.jupyter_deployments[0]
        try:
            assert jupyter.local_port != jupyter_2.local_port
            check_local_http_connection(port=jupyter.local_port)
            check_local_http_connection(port=jupyter_2.local_port)
        finally:
            assert isinstance(jupyter_2, JupyterDeploymentImpl)
            jupyter_2.cancel_local()


def test_cancelled_node_allocation_is_discarded_on_pull():
    user = USER_48
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        stack.enter_context(cancel_on_exit(nodes))
        node = nodes[0]
        nodes.wait(timeout=10)

        local_port = 2223
        jupyter = node.deploy_notebook(local_port=local_port)
        try:
            deployments = cluster.pull_deployments()
            assert not deployments.jupyter_deployments

            cluster.push_deployment(deployment=jupyter)

            jupyter.cancel()
            jupyter = None

            deployments = cluster.pull_deployments()
            assert not deployments.jupyter_deployments
        finally:
            if jupyter is not None:
                jupyter.cancel()

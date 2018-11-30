from contextlib import ExitStack

from idact import show_cluster, deploy_dask
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from tests.helpers.check_http_connection import check_http_connection
from tests.helpers.clear_deployment_sync_data import clear_deployment_sync_data
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_55, USER_56
from tests.helpers.testing_environment import TEST_CLUSTER


def test_able_to_sync_dask():
    user = USER_55
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        stack.enter_context(cancel_on_exit(nodes))
        nodes.wait(timeout=10)

        dask = deploy_dask(nodes)
        stack.enter_context(cancel_on_exit(dask))

        deployments = cluster.pull_deployments()
        assert not deployments.dask_deployments

        cluster.push_deployment(deployment=dask)
        deployments = cluster.pull_deployments()
        print(deployments)

        assert len(deployments.dask_deployments) == 1
        dask_2 = deployments.dask_deployments[0]
        try:
            assert dask.diagnostics.addresses != dask_2.diagnostics.addresses
            for url in dask.diagnostics.addresses:
                check_http_connection(url=url)
            for url in dask_2.diagnostics.addresses:
                check_http_connection(url=url)
        finally:
            dask_2.cancel_local()


def test_cancelled_dask_allocation_is_discarded_on_pull():
    user = USER_56
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))
        stack.enter_context(clear_deployment_sync_data(user))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        stack.enter_context(cancel_on_exit(nodes))
        nodes.wait(timeout=10)

        dask = deploy_dask(nodes)
        stack.enter_context(cancel_on_exit(dask))

        try:
            deployments = cluster.pull_deployments()
            assert not deployments.jupyter_deployments

            cluster.push_deployment(deployment=dask)

            dask.cancel()
            dask = None

            deployments = cluster.pull_deployments()
            assert not deployments.jupyter_deployments
        finally:
            if dask is not None:
                dask.cancel()

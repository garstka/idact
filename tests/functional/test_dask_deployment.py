from contextlib import ExitStack, contextmanager
from pprint import pprint

import fabric.network
import requests
from bitmath import MiB

from idact import show_cluster, Walltime, Nodes
from idact.core.deploy_dask import deploy_dask
from idact.detail.auth.set_password import set_password
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_18, USER_17
from tests.helpers.testing_environment import TEST_CLUSTER


@contextmanager
def deploy_dask_on_testing_cluster(nodes: Nodes):
    ps_dask_worker = "ps -u $USER | grep [d]ask-worker ; exit 0"
    ps_dask_scheduler = "ps -u $USER | grep [d]ask-scheduler ; exit 0"

    node = nodes[0]
    deployment = None
    try:
        nodes.wait(timeout=10)
        assert nodes.running()

        deployment = deploy_dask(nodes=nodes)
        print(deployment)

        fabric.network.disconnect_all()

        ps_lines = node.run(ps_dask_scheduler).splitlines()
        pprint(ps_lines)
        assert len(ps_lines) == 1

        ps_lines = node.run(ps_dask_worker).splitlines()
        pprint(ps_lines)
        assert len(ps_lines) == 2

        client = deployment.get_client()
        print(client)

        def inc(value):
            return value + 1

        result_x = client.submit(inc, 10)
        print(result_x)
        mapped = client.map(inc, range(100))
        print(mapped)

        assert result_x.result() == 11
        assert client.gather(mapped) == list(range(1, 101))

        pprint(deployment.diagnostics.addresses)

        for address in deployment.diagnostics.addresses:
            request = requests.get(address)
            assert "text/html" in request.headers['Content-type']

        try:
            yield node
        finally:
            deployment.cancel()

            ps_lines = node.run(ps_dask_scheduler).splitlines()
            pprint(ps_lines)
            assert not ps_lines

            ps_lines = node.run(ps_dask_worker).splitlines()
            pprint(ps_lines)
            assert not ps_lines

        deployment = None
    finally:
        try:
            if deployment is not None:
                deployment.cancel()
        finally:
            nodes.cancel()


def test_dask_deployment():
    user = USER_17
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=2,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))

        with deploy_dask_on_testing_cluster(nodes):
            pass


def test_dask_deployment_with_setup_actions():
    user = USER_18
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=2,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))

        cluster.config.setup_actions.dask = ['echo ABC > file.txt',
                                             'mv file.txt file2.txt']
        with deploy_dask_on_testing_cluster(nodes) as node:
            assert node.run("cat file2.txt") == "ABC"

from contextlib import ExitStack
from pprint import pprint
from time import sleep

import fabric.network
import requests
from bitmath import MiB

from idact import show_cluster, Walltime
from idact.detail.auth.set_password import set_password
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment, TEST_CLUSTER
from tests.helpers.test_users import get_test_user_password, USER_6


def test_jupyter_hub_deployment():
    user = USER_6
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
        deployment = None
        try:
            nodes.wait(timeout=10)
            assert nodes.running()

            local_port = 2223
            deployment = node.deploy_notebook(local_port=local_port)
            print(deployment)

            assert deployment.local_port == local_port

            fabric.network.disconnect_all()

            ps_jupyter_lines = node.run(
                "ps -ef -u $USER | grep jupyterhub").splitlines()
            pprint(ps_jupyter_lines)
            assert len(ps_jupyter_lines) == 3

            ps_proxy_lines = node.run(
                "ps -ef -u $USER | grep configurable-http-proxy").splitlines()
            pprint(ps_proxy_lines)
            assert len(ps_proxy_lines) == 3

            sleep(3)
            request = requests.get("http://127.0.0.1:{local_port}".format(
                local_port=local_port))
            assert "text/html" in request.headers['Content-type']

            deployment.cancel()

            ps_jupyter_lines = node.run(
                "ps -ef -u $USER | grep jupyterhub").splitlines()
            pprint(ps_jupyter_lines)
            assert len(ps_jupyter_lines) == 2

            ps_proxy_lines = node.run(
                "ps -ef -u $USER | grep configurable-http-proxy").splitlines()
            pprint(ps_proxy_lines)
            assert len(ps_proxy_lines) == 2

            deployment = None
        finally:
            try:
                if deployment is not None:
                    deployment.cancel()
            finally:
                nodes.cancel()

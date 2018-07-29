from contextlib import ExitStack
from pprint import pprint

import fabric.network
import requests
from bitmath import MiB

from idact import show_cluster, Walltime
from idact.detail.auth.set_password import set_password
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_6
from tests.helpers.testing_environment import TEST_CLUSTER


def test_jupyter_hub_deployment():
    user = USER_6
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))

        ps_jupyterhub = ("ps -ef -u $USER |"
                         " grep '[/]usr/bin/python3.6 /usr/bin/jupyterhub'"
                         "; exit 0")

        ps_proxy = ("ps -ef -u $USER |"
                    " grep '[n]ode /usr/bin/configurable-http-proxy'"
                    "; exit 0")

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

            ps_jupyter_lines = node.run(ps_jupyterhub).splitlines()
            pprint(ps_jupyter_lines)
            assert len(ps_jupyter_lines) == 1

            ps_proxy_lines = node.run(ps_proxy).splitlines()
            pprint(ps_proxy_lines)
            assert len(ps_proxy_lines) == 1

            request = requests.get("http://127.0.0.1:{local_port}".format(
                local_port=local_port))
            assert "text/html" in request.headers['Content-type']

            deployment.cancel()

            ps_jupyter_lines = node.run(ps_jupyterhub).splitlines()
            pprint(ps_jupyter_lines)
            assert not ps_jupyter_lines

            ps_proxy_lines = node.run(ps_proxy).splitlines()
            pprint(ps_proxy_lines)
            assert not ps_proxy_lines

            deployment = None

        finally:
            try:
                if deployment is not None:
                    deployment.cancel()
            finally:
                nodes.cancel()

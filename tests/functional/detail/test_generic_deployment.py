from contextlib import ExitStack

import fabric.network
import pytest
from bitmath import MiB

from idact import show_cluster, Walltime
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.deploy_generic import deploy_generic
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment, TEST_CLUSTER
from tests.helpers.test_users import USER_7, get_test_user_password


def test_generic_deployment():
    user = USER_7
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        print(cluster)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        node = nodes[0]
        deployment = None
        try:
            nodes.wait(timeout=10)
            assert nodes.running()

            command = "echo ABC && sleep 3 && echo DEF && sleep 15 && echo GHI"
            deployment = deploy_generic(node=node,
                                        command=command,
                                        capture_output_seconds=4)
            print(deployment)

            assert deployment.output == "ABC\nDEF"

            fabric.network.disconnect_all()
            node.run(
                "kill -0 {pid}".format(pid=deployment.pid))

            deployment.cancel()
            with pytest.raises(RuntimeError):
                node.run(
                    "kill -0 {pid}".format(pid=deployment.pid))

            deployment = None

        finally:
            try:
                if deployment is not None:
                    deployment.cancel()
            finally:
                nodes.cancel()

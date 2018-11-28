from contextlib import ExitStack

import pytest
from bitmath import MiB

from idact import show_cluster, Walltime
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.create_deployment_dir import create_runtime_dir
from idact.detail.deployment.deploy_generic import deploy_generic
from idact.detail.helper.remove_runtime_dir \
    import remove_runtime_dir_on_failure
from idact.detail.nodes.node_internal import NodeInternal
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_7, get_test_user_password
from tests.helpers.testing_environment import TEST_CLUSTER


def test_generic_deployment():
    user = USER_7
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        print(cluster)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))
        node = nodes[0]

        nodes.wait(timeout=10)
        assert nodes.running()

        assert isinstance(node, NodeInternal)
        runtime_dir = create_runtime_dir(node=node)
        stack.enter_context(
            remove_runtime_dir_on_failure(node=node,
                                          runtime_dir=runtime_dir))
        script_contents = "echo ABC && sleep 30"

        assert isinstance(node, NodeInternal)
        deployment = deploy_generic(node=node,
                                    script_contents=script_contents,
                                    runtime_dir=runtime_dir)
        with cancel_on_exit(deployment):
            print(deployment)

            node.run(
                "kill -0 {pid}".format(pid=deployment.pid))

        with pytest.raises(RuntimeError):
            node.run(
                "kill -0 {pid}".format(pid=deployment.pid))

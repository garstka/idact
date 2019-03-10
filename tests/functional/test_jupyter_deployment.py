from contextlib import ExitStack, contextmanager
from pprint import pprint

from bitmath import MiB

from idact import show_cluster, Walltime, Nodes
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.get_free_local_port import get_free_local_port
from idact.detail.helper.retry import retry
from tests.helpers.check_http_connection import check_local_http_connection
from tests.helpers.check_no_output import check_no_output
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_6, USER_16, \
    USER_58
from tests.helpers.testing_environment import TEST_CLUSTER, \
    SLURM_WAIT_TIMEOUT, get_testing_process_count


@contextmanager
def deploy_jupyter(nodes: Nodes):
    ps_jupyter = "ps -u $USER | grep jupyter ; exit 0"

    node = nodes[0]
    nodes.wait(timeout=SLURM_WAIT_TIMEOUT)
    assert nodes.running()

    local_port = get_free_local_port()
    deployment = node.deploy_notebook(local_port=local_port)
    with cancel_on_exit(deployment):
        print(deployment)
        assert str(deployment) == repr(deployment)

        assert deployment.local_port == local_port

        ps_jupyter_lines = node.run(ps_jupyter).splitlines()
        pprint(ps_jupyter_lines)
        assert len(ps_jupyter_lines) == 1

        check_local_http_connection(port=local_port)

        yield node

    retry(lambda: check_no_output(node=node, command=ps_jupyter),
          retries=5 * get_testing_process_count(), seconds_between_retries=1)


def test_jupyter_deployment():
    user = USER_6
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))

        with deploy_jupyter(nodes):
            pass


def test_jupyter_deployment_with_setup_actions():
    user = USER_16
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))

        cluster.config.setup_actions.jupyter = ['echo ABC > file.txt',
                                                'mv file.txt file2.txt']
        with deploy_jupyter(nodes) as node:
            assert node.run("cat file2.txt") == "ABC"


def test_jupyter_deployment_not_lab():
    user = USER_58
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        assert cluster.config.use_jupyter_lab
        cluster.config.use_jupyter_lab = False

        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))

        with deploy_jupyter(nodes):
            pass

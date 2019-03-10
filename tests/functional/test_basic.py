from contextlib import ExitStack

import bitmath
from bitmath import MiB
import pytest

from idact import show_clusters, show_cluster, Walltime
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_1, get_test_user_password, USER_22, \
    USER_23
from tests.helpers.testing_environment import TEST_CLUSTER, SLURM_WAIT_TIMEOUT


def test_basic():
    user = USER_1
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        clusters = show_clusters()
        print(clusters)

        assert len(clusters) == 1

        cluster = show_cluster(name=TEST_CLUSTER)
        print(cluster)

        assert clusters[TEST_CLUSTER] == cluster

        nodes = cluster.allocate_nodes(nodes=2,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30),
                                       native_args={
                                           '--partition': 'debug'
                                       })
        with cancel_on_exit(nodes):
            assert len(nodes) == 2
            assert nodes[0] in nodes
            print(nodes)
            assert str(nodes) == repr(nodes)

            nodes.wait(timeout=SLURM_WAIT_TIMEOUT)
            assert nodes.running()

            print(nodes)
            print(nodes[0])

            assert nodes[0].run('whoami') == user
            assert nodes[1].run('whoami') == user

        assert not nodes.running()
        with pytest.raises(RuntimeError):
            nodes.wait()
        with pytest.raises(RuntimeError):
            nodes[0].run('whoami')


def test_allocate_defaults():
    user = USER_22
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes()
        stack.enter_context(cancel_on_exit(nodes))
        assert len(nodes) == 1
        node = nodes[0]

        nodes.wait(timeout=SLURM_WAIT_TIMEOUT)
        assert nodes.running()

        assert node.resources.cpu_cores == 1
        assert node.resources.memory_total == bitmath.GiB(1)
        print(node)

        assert node.run('whoami') == user


def test_allocate_with_string_params():
    user = USER_23
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location(user))
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)

        nodes = cluster.allocate_nodes(walltime='0:10:00',
                                       memory_per_node='500MiB')
        stack.enter_context(cancel_on_exit(nodes))
        assert len(nodes) == 1
        node = nodes[0]

        nodes.wait(timeout=SLURM_WAIT_TIMEOUT)
        assert nodes.running()

        assert node.resources.cpu_cores == 1
        assert node.resources.memory_total == bitmath.MiB(500)
        print(node)

        assert node.run('whoami') == user

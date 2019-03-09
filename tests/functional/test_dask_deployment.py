import sys
from contextlib import ExitStack, contextmanager
from pprint import pprint

import dask.distributed
import pytest
import requests
from bitmath import MiB

import idact.detail.dask.deploy_dask_impl
from idact import show_cluster, Walltime, Nodes, Node
from idact.core.deploy_dask import deploy_dask
from idact.detail.auth.set_password import set_password
from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.retry import retry
from tests.helpers.check_no_output import check_no_output
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.save_opened_in import save_opened_in
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import get_test_user_password, USER_18, \
    USER_17, USER_20, USER_24, USER_41, USER_42
from tests.helpers.testing_environment import TEST_CLUSTER


def check_submission_works(node: Node, client: dask.distributed.Client):
    print("Testing task submission.")

    local_version = [i for i in sys.version_info[0:3]]
    print("Local version: {}".format(local_version))

    python_executable = "python{major}.{minor}".format(major=local_version[0],
                                                       minor=local_version[1])

    print(
        "Will try to find out the version"
        " of python executable: {python_executable}".format(
            python_executable=python_executable))
    print("If this fails, make sure the testing setup has"
          " the same, or close Python version"
          " (major and minor version components must match).")

    command = (
        "{python_executable} -c 'import sys;"
        " print(\"\\n\".join("
        "[str(i) for i in sys.version_info[0:3]]))'".format(
            python_executable=python_executable))

    remote_version = [int(i) for i in node.run(command).splitlines()]

    print("Remote version: {}".format(remote_version))

    if local_version != remote_version:
        print("Python version mismatch: local {} vs remote {}".format(
            local_version, remote_version))

    print("If the task submission fails, make sure the testing setup has"
          " the same, or close Python version.")
    print("Update the local Python installation if possible.")
    print("If this still doesn't work, update your Dask library.")

    def inc(value):
        return value + 1

    result_x = client.submit(inc, 10)
    print(result_x)
    mapped = client.map(inc, range(100))
    print(mapped)

    assert result_x.result() == 11
    assert client.gather(mapped) == list(range(1, 101))


@contextmanager
def deploy_dask_on_testing_cluster(nodes: Nodes):
    ps_dask_worker = "ps -u $USER | grep [d]ask-worker ; exit 0"
    ps_dask_scheduler = "ps -u $USER | grep [d]ask-scheduler ; exit 0"

    node = nodes[0]
    nodes.wait(timeout=10)
    assert nodes.running()

    deployment = deploy_dask(nodes=nodes)
    with cancel_on_exit(deployment):
        print(deployment)
        assert str(deployment) == repr(deployment)

        ps_lines = node.run(ps_dask_scheduler).splitlines()
        pprint(ps_lines)
        assert len(ps_lines) == 1

        ps_lines = node.run(ps_dask_worker).splitlines()
        pprint(ps_lines)
        assert len(ps_lines) == len(nodes)

        client = deployment.get_client()
        print(client)

        check_submission_works(node=node, client=client)

        pprint(deployment.diagnostics.addresses)
        assert len(deployment.diagnostics.addresses) == len(nodes) + 1

        for address in deployment.diagnostics.addresses:
            request = requests.get(address)
            assert "text/html" in request.headers['Content-type']

        opened_addresses = []
        with save_opened_in(opened_addresses):
            deployment.diagnostics.open_all()

        assert opened_addresses == deployment.diagnostics.addresses

        yield node

    retry(lambda: check_no_output(node=node, command=ps_dask_scheduler),
          retries=5, seconds_between_retries=1)

    retry(lambda: check_no_output(node=node, command=ps_dask_worker),
          retries=5, seconds_between_retries=1)


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
        stack.enter_context(cancel_on_exit(nodes))

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
        stack.enter_context(cancel_on_exit(nodes))

        cluster.config.setup_actions.dask = ['echo ABC > file.txt',
                                             'mv file.txt file2.txt']
        with deploy_dask_on_testing_cluster(nodes) as node:
            assert node.run("cat file2.txt") == "ABC"


def test_cannot_deploy_dask_on_zero_nodes():
    user = USER_20
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        print(show_cluster(name=TEST_CLUSTER))
        with pytest.raises(ValueError):
            deploy_dask(nodes=[])


def test_dask_deployment_with_absolute_scratch_path():
    user = USER_24
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        cluster.config.scratch = '/home/user-24'

        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=10))
        stack.enter_context(cancel_on_exit(nodes))

        with deploy_dask_on_testing_cluster(nodes):
            pass


def test_dask_deployment_with_redeploy_on_validation_failure():
    user = USER_41
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
        stack.enter_context(cancel_on_exit(nodes))

        assert idact.detail.dask.deploy_dask_impl.validate_worker
        stored_validate_worker = \
            idact.detail.dask.deploy_dask_impl.validate_worker

        fake_validation_counter = [0]

        def fake_validate_worker(worker: DaskWorkerDeployment):
            current_count = fake_validation_counter[0]
            fake_validation_counter[0] = current_count + 1

            print("Fake worker validation.")
            if current_count == 0:
                raise RuntimeError("Fake worker validation: First node fail.")
            print("Defaulting to real worker validation.")
            stored_validate_worker(worker=worker)

        try:
            idact.detail.dask.deploy_dask_impl.validate_worker = \
                fake_validate_worker

            with deploy_dask_on_testing_cluster(nodes):
                pass

            assert fake_validation_counter[0] == 3

        finally:
            idact.detail.dask.deploy_dask_impl.validate_worker = \
                stored_validate_worker


def test_dask_deployment_with_redeploy_failure():
    user = USER_42
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
        stack.enter_context(cancel_on_exit(nodes))

        assert idact.detail.dask.deploy_dask_impl.validate_worker
        stored_validate_worker = \
            idact.detail.dask.deploy_dask_impl.validate_worker

        def fake_validate_worker(worker: DaskWorkerDeployment):
            print("Fake worker validation.")
            raise ValueError("Fake worker validation fail.")

        try:
            idact.detail.dask.deploy_dask_impl.validate_worker = \
                fake_validate_worker

            with pytest.raises(RuntimeError):
                with deploy_dask_on_testing_cluster(nodes):
                    pass

        finally:
            idact.detail.dask.deploy_dask_impl.validate_worker = \
                stored_validate_worker

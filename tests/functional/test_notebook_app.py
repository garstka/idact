import logging
import os
from contextlib import ExitStack, contextmanager
from typing import List

from click.testing import CliRunner, Result

from idact import show_cluster, save_environment, set_log_level, AuthMethod
from idact.detail.auth.set_password import set_password
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.notebook import main
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_49, get_test_user_password, \
    USER_50, USER_51, USER_52
from tests.helpers.testing_environment import TEST_CLUSTER


@contextmanager
def run_notebook_app(user: str,
                     environment_file: str,
                     args: List[str],
                     notebook_defaults: dict = None) -> Result:
    """Runs the notebook app. Returns the result from CliRunner."""
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(set_up_key_location())
        stack.enter_context(reset_environment(
            user=user,
            auth=AuthMethod.PUBLIC_KEY))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        cluster.get_access_node().connect()
        set_log_level(logging.INFO)
        if notebook_defaults:
            config = cluster.config
            assert isinstance(config, ClusterConfigImpl)
            config.notebook_defaults = notebook_defaults
        save_environment(path=environment_file)

        try:
            runner = CliRunner()
            opened_in_browser = []

            def fake_open_in_browser(_):
                opened_in_browser.append(True)

            saved_open_in_browser = JupyterDeploymentImpl.open_in_browser
            JupyterDeploymentImpl.open_in_browser = fake_open_in_browser
            try:
                result = runner.invoke(main, args=args)
            finally:
                JupyterDeploymentImpl.open_in_browser = saved_open_in_browser
            print("\n\n\nClick output of the notebook app run:")
            print(result.output)
            yield result
        finally:
            os.remove(environment_file)


def test_notebook_app_run():
    user = USER_49
    environment_file = './idact.test.conf'
    args = [TEST_CLUSTER,
            '--environment', environment_file,
            '--walltime', '0:00:45']
    with run_notebook_app(user=user,
                          environment_file=environment_file,
                          args=args) as result:
        output = result.output
        assert "Loading environment." in output
        assert "Resetting allocation parameters to defaults." not in output
        assert "Saving defaults." not in output
        assert "Nodes: 1\n" in output
        assert "Cores: 1\n" in output
        assert "Memory per node: 1GiB\n" in output
        assert "Walltime: 0:00:45\n" in output
        assert "No native arguments." in output
        assert "Allocating nodes." in output
        assert "Pushing the allocation deployment." in output
        assert "Pushing the notebook deployment." in output
        assert ("To access the allocation and notebook"
                " deployments from cluster, you can use"
                " the following snippet.") in output
        assert "Notebook address: http://localhost:" in output
        assert "Nodes are still running." in output
        assert "Nodes are no longer running." in output
        assert result.exit_code == 0


def get_different_notebook_defaults_for_test():
    return {'nodes': '2',
            'cores': '1',
            'memory_per_node': '500MiB',
            'native_args': [['--partition'], ['debug']]}


def check_output_with_changed_allocation_parameters(output: str):
    assert "Loading environment." in output
    assert "Resetting allocation parameters to defaults." not in output
    assert "Saving defaults." in output
    assert "Nodes: 2\n" in output
    assert "Cores: 2\n" in output
    assert "Memory per node: 500MiB\n" in output
    assert "Walltime: 0:00:45\n" in output
    assert "Native arguments:" in output
    assert "--partition -> debug" in output
    assert "Allocating nodes." in output
    assert "Pushing the allocation deployment." in output
    assert "Pushing the notebook deployment." in output
    assert ("To access the allocation and notebook"
            " deployments from cluster, you can use"
            " the following snippet.") in output
    assert "Notebook address: http://localhost:" in output
    assert "Nodes are still running." in output
    assert "Nodes are no longer running." in output


def test_notebook_app_run_save_defaults():
    user = USER_50
    environment_file = './idact.test.conf'
    args = [TEST_CLUSTER,
            '--environment', environment_file,
            '--walltime', '0:00:45',
            '--save-defaults',
            '--nodes', '2',
            '--cores', '1',
            '--memory-per-node', '500MiB',
            '--native-arg', '--partition', 'debug']
    with run_notebook_app(user=user,
                          environment_file=environment_file,
                          args=args) as result:
        output = result.output
        assert "Loading environment." in output
        assert "Resetting allocation parameters to defaults." not in output
        assert "Saving defaults." in output
        assert "Nodes: 2\n" in output
        assert "Cores: 1\n" in output
        assert "Memory per node: 500MiB\n" in output
        assert "Walltime: 0:00:45\n" in output
        assert "Native arguments:" in output
        assert "--partition -> debug" in output
        assert "Allocating nodes." in output
        assert "Pushing the allocation deployment." in output
        assert "Pushing the notebook deployment." in output
        assert ("To access the allocation and notebook"
                " deployments from cluster, you can use"
                " the following snippet.") in output
        assert "Notebook address: http://localhost:" in output
        assert "Nodes are still running." in output
        assert "Nodes are no longer running." in output
        assert result.exit_code == 0


def test_notebook_app_run_use_defaults():
    user = USER_51
    environment_file = './idact.test.conf'
    args = [TEST_CLUSTER,
            '--environment', environment_file,
            '--walltime', '0:00:45']
    notebook_defaults = get_different_notebook_defaults_for_test()
    with run_notebook_app(user=user,
                          environment_file=environment_file,
                          args=args,
                          notebook_defaults=notebook_defaults) as result:
        output = result.output
        assert "Loading environment." in output
        assert "Resetting allocation parameters to defaults." not in output
        assert "Saving defaults." not in output
        assert "Nodes: 2\n" in output
        assert "Cores: 1\n" in output
        assert "Memory per node: 500MiB\n" in output
        assert "Walltime: 0:00:45\n" in output
        assert "Native arguments:" in output
        assert "--partition -> debug" in output
        assert "Allocating nodes." in output
        assert "Pushing the allocation deployment." in output
        assert "Pushing the notebook deployment." in output
        assert ("To access the allocation and notebook"
                " deployments from cluster, you can use"
                " the following snippet.") in output
        assert "Notebook address: http://localhost:" in output
        assert "Nodes are still running." in output
        assert "Nodes are no longer running." in output
        assert result.exit_code == 0


def test_notebook_app_run_reset_defaults():
    user = USER_52
    environment_file = './idact.test.conf'
    args = [TEST_CLUSTER,
            '--environment', environment_file,
            '--walltime', '0:00:45',
            '--reset-defaults']
    notebook_defaults = get_different_notebook_defaults_for_test()
    with run_notebook_app(user=user,
                          environment_file=environment_file,
                          args=args,
                          notebook_defaults=notebook_defaults) as result:
        output = result.output
        assert "Loading environment." in output
        assert "Resetting allocation parameters to defaults." in output
        assert "Saving defaults." not in output
        assert "Nodes: 1\n" in output
        assert "Cores: 1\n" in output
        assert "Memory per node: 1GiB\n" in output
        assert "Walltime: 0:00:45\n" in output
        assert "No native arguments." in output
        assert "Allocating nodes." in output
        assert "Pushing the allocation deployment." in output
        assert "Pushing the notebook deployment." in output
        assert ("To access the allocation and notebook"
                " deployments from cluster, you can use"
                " the following snippet.") in output
        assert "Notebook address: http://localhost:" in output
        assert "Nodes are still running." in output
        assert "Nodes are no longer running." in output
        assert result.exit_code == 0

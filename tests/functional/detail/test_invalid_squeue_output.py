from contextlib import ExitStack

from idact import show_cluster
from idact.detail.auth.set_password import set_password
from idact.detail.helper.utc_now import utc_now
from idact.detail.slurm.run_squeue import extract_squeue_line
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.test_users import get_test_user_password, USER_62, \
    USER_63, USER_64
from tests.helpers.testing_environment import TEST_CLUSTER


def run_invalid_squeue_output_test(user: str, output: str):
    with ExitStack() as stack:
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)

        assert extract_squeue_line(now=utc_now(),
                                   line=output,
                                   node=cluster.get_access_node()) is None


def test_extract_squeue_invalid_timestamp():
    user = USER_62
    run_invalid_squeue_output_test(user=user,
                                   output="527|1|wrong|None|c1|RUNNING")


def test_extract_squeue_invalid_job_id():
    user = USER_63
    run_invalid_squeue_output_test(user=user,
                                   output="wrong|1|9:54|None|c1|RUNNING")


def test_extract_squeue_invalid_node_count():
    user = USER_64
    run_invalid_squeue_output_test(user=user,
                                   output="527|wrong|9:54|None|c1|RUNNING")

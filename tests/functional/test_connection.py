from fabric.decorators import task
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute

from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.test_users import USER_29, get_test_user_password
from tests.helpers.testing_environment import get_testing_port, \
    get_testing_host


def test_connection():
    @task
    def task_1():
        return run('squeue')

    try:
        user = USER_29
        host = "{user}@{host}:{port}".format(user=user,
                                             host=get_testing_host(),
                                             port=get_testing_port())
        password = get_test_user_password(user)

        with disable_pytest_stdin():
            env.password = password
            result = execute(task_1, hosts=[host])
            print('Result:')
            print(result)

        assert result[host].splitlines()[0] == (
            'JOBID PARTITION     NAME     USER ST       '
            'TIME  NODES NODELIST(REASON)')
    finally:
        env.password = None

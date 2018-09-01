from fabric.decorators import task
from fabric.network import disconnect_all
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute

from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.test_users import USER_29, get_test_user_password


def test_connection():
    @task
    def task_1():
        return run('squeue')

    try:
        user = USER_29
        host = "{user}@localhost:2222".format(user=user)
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
        disconnect_all()

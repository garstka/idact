from fabric.context_managers import hide
from fabric.decorators import task
from fabric.network import disconnect_all
from fabric.operations import run
from fabric.tasks import execute

from idact.detail.auth.set_password import set_password
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin


def test_connection():
    @task
    def task_1():
        return run('squeue')

    try:
        host = 'user-1@localhost:2222'
        password = 'pass-1'

        with hide('everything'):
            with disable_pytest_stdin():
                with set_password(password):
                    result = execute(task_1, hosts=[host])
        print('Result:')
        print(result)

        assert result[host].splitlines()[0] == (
            'JOBID PARTITION     NAME     USER ST       '
            'TIME  NODES NODELIST(REASON)')
    finally:
        disconnect_all()

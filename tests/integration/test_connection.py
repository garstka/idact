from fabric.context_managers import hide
from fabric.decorators import task
from fabric.network import disconnect_all
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute

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
                env.password = password
                result = execute(task_1, hosts=[host])
        print('Result:')
        print(result)

        assert result[host] == ('JOBID PARTITION     NAME     USER ST       '
                                'TIME  NODES NODELIST(REASON)')
    finally:
        disconnect_all()

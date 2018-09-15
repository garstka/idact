from time import sleep

from tests.helpers.paramiko_connect import paramiko_connect

STARTUP_TIME = 1


def start_stress_cpu(user: str, timeout: int = 10):
    """Runs a remote command that stresses the CPU, with a timeout.

        :param user: User to run stress as.

        :param timeout: Stress timeout.

    """
    with paramiko_connect(user=user) as ssh:
        ssh.exec_command("nohup stress --cpu 1 --timeout {timeout} &".format(
            timeout=timeout))
        sleep(STARTUP_TIME)


def stop_stress_cpu(user: str):
    """Stops commands stressing the CPU.

        :param user: User with a running stress command.

    """
    with paramiko_connect(user=user) as ssh:
        ssh.exec_command("killall stress")

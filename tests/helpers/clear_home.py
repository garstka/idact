from tests.helpers.paramiko_connect import paramiko_connect


def clear_home(user: str):
    """Clears the home directory."""
    with paramiko_connect(user=user) as ssh:
        ssh.exec_command(command="rm -rf ~/.ssh")

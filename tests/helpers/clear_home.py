from tests.helpers.paramiko_connect import paramiko_connect


def clear_home(user: str):
    """Clears the user's home directory.

        Removes the `.ssh` dir.

        :param user: User, whose home directory should be cleared.

    """
    with paramiko_connect(user=user) as ssh:
        ssh.exec_command(command="rm -rf ~/.ssh")

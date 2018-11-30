"""This module contains a function for building a command that runs
    a deployment script."""

import shlex


def get_deployment_command(script_path: str) -> str:
    """Returns a command that runs the given script in a background
        process and returns its PID.

        :param script_path: Path to the script to run.

    """
    script_path_quoted = shlex.quote(script_path)

    # - Runs the script in a new shell in the background.
    # - nohup is used, so the script can still run after top shell exits.
    # - Redirects stderr of the background script to stdout.
    # - Redirects stdout of the background script to /dev/null.
    # - Prints the background shell's pid to stdout.
    run = ("nohup bash {script_path_quoted} > /dev/null 2>&1"
           " & echo $!").format(script_path_quoted=script_path_quoted)
    return run

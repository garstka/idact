"""This module contains a function for building a command that runs
    a deployment script."""

import re
import shlex

AMPERSAND_REGEX = r'([^&]|^)&([^&]|$)'
AMPERSAND_REGEX_COMPILED = re.compile(AMPERSAND_REGEX)
TIME_TO_OUTPUT_PID = 1


def get_deployment_command(script_path: str,
                           capture_output_seconds: int = 1) -> str:
    """Returns a command that runs the given script in a background
        process and returns its PID.

        :param script_path: Path to the script to run.

        :param capture_output_seconds: Time to capture initial command output.

    """
    if capture_output_seconds < 0:
        raise ValueError("Capture time cannot be negative")
    script_path_quoted = shlex.quote(script_path)

    # - Runs the script in a new shell in the background.
    # - nohup is used, so the script can still run after top shell exits.
    # - Redirects stderr of the background script to stdout.
    # - Redirects stdout of the background script to file descriptor 3.
    # - Prints the background shell's pid to stdout.
    # - Removes the background script.
    # - Reads from the descriptor containing stdout of the background script.
    # - Sets timeout, so only the first few seconds of the output are captured,
    #  and the ssh command doesn't have to wait for the background script
    #  to finish.
    run = ("exec 3< <(nohup bash -c"
           " 'sleep {time_to_output_pid};'{script_path_quoted} 2>&1)"
           " ; echo $!"
           " ; timeout {capture_output_seconds} cat <&3"
           " ; rm -f {script_path_quoted}"
           " ; exit 0").format(time_to_output_pid=TIME_TO_OUTPUT_PID,
                               script_path_quoted=script_path_quoted,
                               capture_output_seconds=(
                                   TIME_TO_OUTPUT_PID + capture_output_seconds
                               ))
    return run

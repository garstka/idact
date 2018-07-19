import re
import shlex

AMPERSAND_REGEX = r'([^&]|^)&([^&]|$)'
AMPERSAND_REGEX_COMPILED = re.compile(AMPERSAND_REGEX)
TIME_TO_OUTPUT_PID = 1


def get_deployment_command(command: str,
                           capture_output_seconds: int = 1) -> str:
    """Returns a command that runs the given command in a background
       bash process after returning its PID.

        :param command: Command to run in the background.

        :param capture_output_seconds: Time to capture initial command output.

    """
    if "'" in command:
        raise ValueError("Single-quote is not allowed in deployment commands.")
    if AMPERSAND_REGEX_COMPILED.search(command):
        raise ValueError("Ampersand is not allowed in deployment commands.")
    if capture_output_seconds < 0:
        raise ValueError("")
    command_quoted = shlex.quote(command)

    # - Runs the command in a new shell in the background.
    # - nohup is used, so the command can still run after top shell exits.
    # - Redirects stderr of the background command to stdout.
    # - Redirects stdout of the background command to file descriptor 3.
    # - Prints the background shell's pid to stdout.
    # - Reads from the descriptor containing stdout of the background command.
    # - Sets timeout, so only the first few seconds of the output are captured,
    #  and the ssh command doesn't have to wait for the background command
    #  to finish.
    run = ("exec 3< <(nohup bash -c"
           " 'sleep {time_to_output_pid};'{command_quoted} 2>&1)"
           " ; echo $!"
           " ; timeout {capture_output_seconds} cat <&3"
           " ; exit 0").format(time_to_output_pid=TIME_TO_OUTPUT_PID,
                               command_quoted=command_quoted,
                               capture_output_seconds=(
                                   TIME_TO_OUTPUT_PID + capture_output_seconds
                               ))
    return run

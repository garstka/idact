#!/usr/bin/env python3
"""Clears the container fingerprint to prevent MITM warnings next time
   the container runs."""

import os
import subprocess as sub
import sys
import traceback

CLEAR_COMMAND = "ssh-keygen -f \"{hosts}\" -R [localhost]:{{SLURM_SSH_PORT}}"
CLEAR_COMMAND = CLEAR_COMMAND.format(
    hosts=os.path.expanduser('~/.ssh/known_hosts'))


def main():
    """Main script function."""
    try:
        clear_command = CLEAR_COMMAND.format(
            SLURM_SSH_PORT=os.environ['SLURM_SSH_PORT'])
        sub.check_call(clear_command, shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

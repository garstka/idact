#!/usr/bin/env python3
"""Performs full testing environment teardown: Stops and removes the container,
   clears ssh keys saved to known_hosts.
"""

import os
import subprocess as sub
import sys
import traceback

WORKING_DIR = os.path.realpath(os.path.dirname(__file__))

PYTHON = sys.executable

COMMANDS = ["docker stop {SLURM_CONTAINER}",
            "docker rm {SLURM_CONTAINER}",
            "{python} ssh_clear_fingerprint.py".format(python=sys.executable)]


def main():
    """Main script function."""
    try:
        os.chdir(WORKING_DIR)

        for command in COMMANDS:
            sub.call(command.format(
                SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

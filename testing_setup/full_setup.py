#!/usr/bin/env python3
"""Performs full testing environment setup: Pulls and runs the container,
   installs an ssh server, adds users.
"""

import os
import subprocess as sub
import sys
import traceback

WORKING_DIR = os.path.realpath(os.path.dirname(__file__))

PYTHON = sys.executable

COMMANDS = [i.format(python=PYTHON) for i in
            ['{python} container_pull.py',
             '{python} container_run.py',
             '{python} ssh_install.py',
             '{python} ssh_generate_host_keys.py',
             '{python} ssh_add_users.py',
             '{python} ssh_run.py']]


def main():
    try:
        os.chdir(WORKING_DIR)
        for command in COMMANDS:
            sub.check_call(command, shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

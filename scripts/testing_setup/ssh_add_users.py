#!/usr/bin/env python3
"""Adds $SLURM_USERS users to the container:
   (user-0, pass-0), (user-1, pass-1), ...
"""

import os
import subprocess as sub
import sys
import traceback

PREFIX = "docker exec {SLURM_CONTAINER} "

USER_COUNT = "{SLURM_USERS}"

ADD_USER_COMMAND = "useradd user-{i}"

SET_PASS_COMMAND = "echo -e 'pass-{i}\\npass-{i}' | passwd --stdin user-{i}"


def main():
    """Main script function."""
    try:
        prefix = PREFIX.format(SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])
        user_count = int(USER_COUNT.format(
            SLURM_USERS=os.environ['SLURM_USERS']))

        add_users = ';'.join([ADD_USER_COMMAND.format(i=i)
                              for i in range(0, user_count)])

        set_pass_commands = ' && '.join([SET_PASS_COMMAND.format(i=i)
                                         for i in range(0, user_count)])
        sub.call(prefix + "bash -c \"{add_users}\"".format(
            add_users=add_users), shell=True)
        sub.check_call(prefix + "bash -c \"{set_pass_commands}\"".format(
            set_pass_commands=set_pass_commands), shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

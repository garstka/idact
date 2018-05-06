#!/usr/bin/env python3
"""Install the ssh daemon in the container."""

import os
import subprocess as sub
import sys
import traceback

PREFIX = "docker exec {SLURM_CONTAINER} "
INSTALL_COMMAND = "yum -y install openssh-server"


def main():
    try:
        prefix = PREFIX.format(SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])
        sub.check_call(prefix + INSTALL_COMMAND, shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Installs `srun` mock. See :mod:`.srun_mock`.

"""

import os
import subprocess as sub
import sys
import traceback

INSTALL_DOS2UNIX = "docker exec {SLURM_CONTAINER} yum -y install dos2unix"

COPY_SCRIPT = "docker cp srun_mock.py {SLURM_CONTAINER}:/usr/local/bin/srun"

SET_PERMISSIONS = "docker exec {SLURM_CONTAINER} chmod 775 /usr/local/bin/srun"

RUN_DOS2UNIX = "docker exec {SLURM_CONTAINER} dos2unix /usr/local/bin/srun"

WORKING_DIR = os.path.realpath(os.path.dirname(__file__))


def main():
    try:
        os.chdir(WORKING_DIR)

        print("Installing dos2unix...")
        sub.check_call(INSTALL_DOS2UNIX.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)
        print("Installing srun mock...")
        sub.check_call(COPY_SCRIPT.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)
        sub.check_call(SET_PERMISSIONS.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)
        sub.check_call(RUN_DOS2UNIX.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

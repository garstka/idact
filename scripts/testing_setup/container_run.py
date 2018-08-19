#!/usr/bin/env python3
"""Runs the container used for testing."""

import os
import subprocess as sub
import sys
import time
import traceback

PULL_CONTAINER_COMMAND = "docker pull {SLURM_IMAGE}"

RUN_COMMAND = "docker run -d -p {SLURM_SSH_PORT}:22 -it -h ernie " \
              "--name {SLURM_CONTAINER} {SLURM_IMAGE}"

ADD_MEMORY_COMMAND = "docker exec {SLURM_CONTAINER} " \
                     "sed -i" \
                     " 's/RealMemory=1000/RealMemory=2000/g'" \
                     " /etc/slurm/slurm.conf"

SLEEP_BEFORE_RESTART = 10

RESTART_COMMAND = "docker exec {SLURM_CONTAINER} " \
                  "supervisorctl restart slurmctld"

STATUS_COMMAND = "docker exec {SLURM_CONTAINER} supervisorctl status"

UPDATE_HOSTS_COMMAND = ('docker exec {SLURM_CONTAINER} bash -c "'
                        'echo 127.0.0.1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10'
                        ' >> /etc/hosts"')


def main():
    """Main script function."""
    try:
        sub.check_call(PULL_CONTAINER_COMMAND.format(
            SLURM_IMAGE=os.environ['SLURM_IMAGE']), shell=True)

        sub.check_call(RUN_COMMAND.format(
            SLURM_SSH_PORT=os.environ['SLURM_SSH_PORT'],
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER'],
            SLURM_IMAGE=os.environ['SLURM_IMAGE']), shell=True)

        sub.check_call(ADD_MEMORY_COMMAND.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)

        time.sleep(SLEEP_BEFORE_RESTART)

        sub.check_call(RESTART_COMMAND.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)

        sub.check_call(STATUS_COMMAND.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)

        sub.check_call(UPDATE_HOSTS_COMMAND.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER']), shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

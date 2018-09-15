#!/usr/bin/env python3
"""Installs stress."""

import os
import subprocess as sub
import sys
import traceback

DOCKER_EXEC = "docker exec {SLURM_CONTAINER} "

COMMAND_INSTALL_STRESS = "yum -y install stress"


def main():
    """Main script function."""
    try:
        docker_exec = DOCKER_EXEC.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])

        print("Installing stress...")
        sub.check_call(docker_exec + COMMAND_INSTALL_STRESS, shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

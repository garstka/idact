#!/usr/bin/env python3
"""Installs Dask, Dask Distributed and bokeh."""

import os
import subprocess as sub
import sys
import traceback

DOCKER_EXEC = "docker exec {SLURM_CONTAINER} "

COMMAND_INSTALL_DASK = "pip3.6 install dask distributed bokeh"


def main():
    try:
        docker_exec = DOCKER_EXEC.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])

        print("Installing Dask, Dask Distributed and bokeh...")
        sub.check_call(docker_exec + COMMAND_INSTALL_DASK, shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Installs Dask, Dask Distributed and bokeh."""

import os
import subprocess as sub
import sys
import traceback

MAJOR, MINOR = sys.version_info[0:2]

DOCKER_EXEC = "docker exec {SLURM_CONTAINER} "

COMMAND_INSTALL_DASK = (
    "python{major}.{minor} -mpip install dask distributed bokeh".format(
        major=MAJOR,
        minor=MINOR))


def main():
    """Main script function."""
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

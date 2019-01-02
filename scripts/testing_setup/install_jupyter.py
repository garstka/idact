#!/usr/bin/env python3
"""Installs Jupyter Notebook, Jupyter Hub and Jupyter Lab."""

import os
import subprocess as sub
import sys
import traceback

MAJOR, MINOR = sys.version_info[0:2]

DOCKER_EXEC = "docker exec {SLURM_CONTAINER} "

COMMANDS_INSTALL_JUPYTER = [
    "python{major}.{minor} -mpip install jupyter".format(
        major=MAJOR,
        minor=MINOR)]

COMMANDS_INSTALL_JUPYTER_HUB = [
    "yum -y install npm",
    "npm config set strict-ssl false",
    "npm install -y -g configurable-http-proxy",
    "python{major}.{minor} -mpip install jupyterhub".format(
        major=MAJOR,
        minor=MINOR)]

COMMANDS_INSTALL_JUPYTER_LAB = [
    "pip{major}.{minor} install jupyterlab".format(
        major=MAJOR,
        minor=MINOR)]


def main():
    """Main script function."""
    try:
        docker_exec = DOCKER_EXEC.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])

        def call(command):
            """Alias for check_call."""
            sub.check_call(docker_exec + command, shell=True)

        print("Installing Jupyter...")
        for i in COMMANDS_INSTALL_JUPYTER:
            call(i)

        print("Installing Jupyter Hub...")
        for i in COMMANDS_INSTALL_JUPYTER_HUB:
            call(i)

        print("Installing Jupyter Lab...")
        for i in COMMANDS_INSTALL_JUPYTER_LAB:
            call(i)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

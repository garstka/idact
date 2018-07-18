#!/usr/bin/env python3
"""Installs Jupyter Notebook, Jupyter Hub and Jupyter Lab."""

import os
import subprocess as sub
import sys
import traceback

DOCKER_EXEC = "docker exec {SLURM_CONTAINER} "

COMMANDS_INSTALL_JUPYTER = ["pip3.6 install jupyter"]

COMMANDS_INSTALL_JUPYTER_HUB = ["yum -y install npm",
                                "npm install -y -g configurable-http-proxy",
                                "pip3.6 install jupyterhub"]

COMMANDS_INSTALL_JUPYTER_LAB = ["pip3.6 install jupyterlab"]


def main():
    try:
        docker_exec = DOCKER_EXEC.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])

        def call(command):
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

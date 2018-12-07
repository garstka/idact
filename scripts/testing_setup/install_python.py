#!/usr/bin/env python3
"""Installs Python 3.6"""

import os
import subprocess as sub
import sys
import traceback

DOCKER_EXEC = "docker exec {SLURM_CONTAINER} "

MAJOR, MINOR = sys.version_info[0:2]

COMMANDS_INSTALL_PYTHON = [
    "yum -y install https://centos{SLURM_CENTOS_VERSION}"
    ".iuscommunity.org/ius-release.rpm".format(
        SLURM_CENTOS_VERSION=os.environ['SLURM_CENTOS_VERSION']),
    "yum -y install"
    " sqlite-devel"
    " python{major}{minor}u"
    " python{major}{minor}u-pip"
    " python{major}{minor}u-devel".format(major=MAJOR,
                                          minor=MINOR)]


def main():
    """Main script function."""
    try:
        docker_exec = DOCKER_EXEC.format(
            SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])

        def call(command):
            """Alias for check_call."""
            sub.check_call(docker_exec + command, shell=True)

        print("Installing Python {major}.{minor}...".format(major=MAJOR,
                                                            minor=MINOR))
        for i in COMMANDS_INSTALL_PYTHON:
            call(i)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

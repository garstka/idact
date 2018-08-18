#!/usr/bin/env python3
"""Installs the ssh daemon in the container."""

import os
import subprocess as sub
import sys
import traceback

PREFIX = "docker exec {SLURM_CONTAINER} "
INSTALL_COMMAND = "yum -y install openssh-server"

SSH_INTERNAL_PORTS = [22, 8022, 8023, 8024, 8025]
APPEND_PORT_COMMAND = "sed -i '$ a\\Port {port}' /etc/ssh/sshd_config"


def main():
    """Main script function."""
    try:
        prefix = PREFIX.format(SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])
        sub.check_call(prefix + INSTALL_COMMAND, shell=True)
        for port in SSH_INTERNAL_PORTS:
            sub.check_call(prefix + APPEND_PORT_COMMAND.format(port=port),
                           shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

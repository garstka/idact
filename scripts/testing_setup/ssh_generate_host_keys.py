#!/usr/bin/env python3
"""Generates host keys for the ssh daemon in the container."""

import os
import subprocess as sub
import sys
import traceback

PREFIX = "docker exec {SLURM_CONTAINER} "

KEY_TYPES = ['rsa', 'dsa', 'ecdsa', 'ed25519']
COMMAND = "bash -c \"echo -e 'y\\n' |" \
          " ssh-keygen -f /etc/ssh/ssh_host_{type}_key -N '' -t {type}\""


def main():
    try:
        prefix = PREFIX.format(SLURM_CONTAINER=os.environ['SLURM_CONTAINER'])
        for key_type in KEY_TYPES:
            sub.check_call(prefix + COMMAND.format(type=key_type), shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

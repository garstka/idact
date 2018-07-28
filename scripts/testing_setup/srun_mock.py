#!/usr/bin/env python3
"""Slurm installation in the container does not support job steps.
   This is why srun should be mostly a passthrough, and provide any expected
   side-effects for tests.

"""

import subprocess as sub
import sys


def main(argv):
    try:
        command_start = argv.index('/bin/bash')
    except ValueError:
        command_start = argv.index('/usr/bin/bash')

    return sub.call(argv[command_start:])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

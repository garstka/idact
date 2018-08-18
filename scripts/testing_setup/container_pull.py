#!/usr/bin/env python3
"""Pulls the container used for testing."""

import os
import subprocess as sub
import sys
import traceback

PULL_CONTAINER_COMMAND = "docker pull {SLURM_IMAGE}"


def main():
    """Main script function."""
    try:
        sub.check_call(PULL_CONTAINER_COMMAND.format(
            SLURM_IMAGE=os.environ['SLURM_IMAGE']), shell=True)
        return 0
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Performs full testing environment teardown: Stops and removes the container,
   clears ssh keys saved to known_hosts.
"""

import os
import subprocess
import sys

WORKING_DIR = os.path.realpath(os.path.dirname(__file__))


def get_stop_command():
    return ['docker', 'stop', os.environ['IDACT_TEST_CONTAINER']]


def get_rm_command():
    return ['docker', 'rm', os.environ['IDACT_TEST_CONTAINER']]


def get_clear_fingerprint_command():
    return [sys.executable, 'ssh_clear_fingerprint.py']


def main():
    """Main script function."""
    os.chdir(WORKING_DIR)

    subprocess.call(get_stop_command())
    subprocess.call(get_rm_command())
    subprocess.call(get_clear_fingerprint_command())


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Clears the container fingerprint to prevent MITM warnings next time
   the container runs."""

import os
import subprocess


def get_clear_command():
    return [
        'ssh-keygen',
        '-f',
        os.path.expanduser('~/.ssh/known_hosts'),
        '-R',
        " [localhost]:{IDACT_TEST_CONTAINER_SSH_PORT}".format(
            IDACT_TEST_CONTAINER_SSH_PORT=os.environ[
                'IDACT_TEST_CONTAINER_SSH_PORT'])]


def main():
    """Main script function."""
    subprocess.check_call(get_clear_command())


if __name__ == '__main__':
    main()

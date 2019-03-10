#!/usr/bin/env python3
"""Runs all tests, `flake8` and `Pylint`."""

import os
import subprocess

import sys

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

PYTEST = "{python} -mpytest -v".format(python=sys.executable)

IDACT_TESTING_PROCESS_COUNT = 4

TESTS_TO_RUN = [
    '{pytest} --flake8 -m flake8'.format(pytest=PYTEST),
    '{pytest} --pylint -m pylint'.format(pytest=PYTEST),
    '{pytest} -n {{jobs}} -vv --cache-clear --cov=idact tests'.format(
        pytest=PYTEST)]


def run(command):
    """Runs a test command and returns the return code.

        :param command: Command to run.
    """
    print("Running '{}':".format(command))
    rc = subprocess.call(command, shell=True)
    print("'{command}' returned {rc}.".format(command=command,
                                              rc=rc))
    return rc


def main(argv):
    """Main script function."""
    os.chdir(WORKING_DIR)

    jobs = argv[2] if len(argv) == 3 and argv[1] == '-n' else 1
    os.environ['IDACT_TESTING_PROCESS_COUNT'] = jobs

    codes = [(command, run(command.format(jobs=jobs)))
             for command in TESTS_TO_RUN]
    failed = [(command, code)
              for command, code in codes if code != 0]

    if not failed:
        print("{total} succeeded.".format(total=len(codes)))
        return 0

    print("{failed}/{total} failed:".format(failed=len(failed),
                                            total=len(codes)))
    for command, code in failed:
        print(" - '{command}' failed with return code {code}."
              .format(command=command, code=code))

    return len(failed)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

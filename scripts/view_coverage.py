#!/usr/bin/env python3
"""Generates coverage and opens report in browser,
   unless --no-show option is set."""

import os
import subprocess as sub
import sys
import webbrowser

COMMANDS_COVERAGE = ['coverage run --source idact -m pytest',
                     'coverage report -m',
                     'coverage html']

COVERAGE_INDEX_PATH = 'htmlcov/index.html'

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))


def main(argv) -> int:
    try:
        no_show = len(argv) == 2 and argv[1] == '--no-show'

        os.chdir(WORKING_DIR)

        print('Generating coverage...')
        for command in COMMANDS_COVERAGE:
            sub.check_call(command, shell=True)

        if not no_show:
            print('Opening docs...')
            webbrowser.open('file://' + os.path.realpath(COVERAGE_INDEX_PATH))

        return 0
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
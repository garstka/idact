#!/usr/bin/env python3
"""Builds sphinx docs and opens index in browser
   unless --no-show option is set."""

import os
import subprocess as sub
import sys
import webbrowser

DOCS_ROOT = 'docs'

COMMAND_GENERATE_API_DOCS = "sphinx-apidoc --force -o {}/ idact".format(
    DOCS_ROOT)

COMMAND_CLEAN_DOCS = 'make clean'
COMMAND_BUILD_DOCS = 'make html'

DOCS_INDEX_PATH = '{}/_build/html/index.html'.format(DOCS_ROOT)

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))


def main(argv):
    try:
        no_show = len(argv) == 2 and argv[1] == '--no-show'

        os.chdir(WORKING_DIR)

        print("Generating API docs with command '{}'...".format(
            COMMAND_GENERATE_API_DOCS))
        sub.check_call(COMMAND_GENERATE_API_DOCS, shell=True)

        os.chdir(DOCS_ROOT)

        print("Cleaning docs with '{}':".format(COMMAND_CLEAN_DOCS))
        sub.check_call(COMMAND_CLEAN_DOCS, shell=True)

        print("Building docs with '{}':".format(COMMAND_BUILD_DOCS))
        sub.check_call(COMMAND_BUILD_DOCS, shell=True)

        os.chdir(WORKING_DIR)

        if not no_show:
            print("Opening docs...")
            webbrowser.open(
                "file://{}".format(os.path.realpath("./" + DOCS_INDEX_PATH)))

        return 0
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))

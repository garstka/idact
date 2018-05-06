#!/usr/bin/env python3
"""Builds sphinx docs and opens index in browser."""

import os
import subprocess as sub
import sys
import webbrowser

DOCS_ROOT = 'docs'

COMMAND_GENERATE_API_DOCS = "sphinx-apidoc -o {}/ idact".format(DOCS_ROOT)
API_DOCS = [DOCS_ROOT + '/modules.rst', DOCS_ROOT + '/idact.rst']

COMMAND_CLEAN_DOCS = 'make clean'
COMMAND_BUILD_DOCS = 'make html'

DOCS_INDEX_PATH = '{}/_build/html/index.html'.format(DOCS_ROOT)

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))


def main():
    try:
        os.chdir(WORKING_DIR)

        for api_doc in API_DOCS:
            if os.path.isfile(api_doc):
                print("Removing '{}'...".format(api_doc))
                os.remove(api_doc)

        print("Generating API docs with command '{}'...".format(
            COMMAND_GENERATE_API_DOCS))
        sub.check_call(COMMAND_GENERATE_API_DOCS, shell=True)

        os.chdir(DOCS_ROOT)

        print("Cleaning docs with '{}':".format(COMMAND_CLEAN_DOCS))
        sub.check_call(COMMAND_CLEAN_DOCS, shell=True)

        print("Building docs with '{}':".format(COMMAND_BUILD_DOCS))
        sub.check_call(COMMAND_BUILD_DOCS, shell=True)

        os.chdir(WORKING_DIR)

        print("Opening docs...")

        print(DOCS_INDEX_PATH)
        print(os.getcwd())
        print("file://{}".format(os.path.realpath("./" + DOCS_INDEX_PATH)))
        webbrowser.open(
            "file://{}".format(os.path.realpath("./" + DOCS_INDEX_PATH)))
        return 0
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

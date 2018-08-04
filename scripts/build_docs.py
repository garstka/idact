#!/usr/bin/env python3
"""Builds sphinx docs and opens the index page in browser
   unless :command:`--no-show` option is set."""

import os
import subprocess as sub
import sys
import webbrowser

DOCS_ROOT = 'docs'

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))


def run_apidoc(module: str):
    """Runs apidoc, generating rst files from code.

        :param module: Module to run apidoc for.
    """
    import better_apidoc
    sys.path.append(WORKING_DIR)
    better_apidoc.main(
        ["better-apidoc",
         "--force",
         "--module-first",
         "--separate",
         "--templates",
         "{docs_root}/_templates".format(docs_root=DOCS_ROOT),
         "-o",
         "{docs_root}/api".format(docs_root=DOCS_ROOT),
         "{working_dir}/{module}".format(working_dir=WORKING_DIR,
                                         module=module)])


SPHINXBUILD = "{python} -msphinx".format(python=sys.executable)

# SPHINXBUILD parameter is for Linux make.
COMMAND_CLEAN_DOCS = 'make clean SPHINXBUILD="{sphinxbuild}"'.format(
    sphinxbuild=SPHINXBUILD)
COMMAND_BUILD_DOCS = 'make html SPHINXBUILD="{sphinxbuild}"'.format(
    sphinxbuild=SPHINXBUILD)

DOCS_INDEX_PATH = '{}/_build/html/index.html'.format(DOCS_ROOT)

MODULES_TO_APIDOC = ['idact',
                     'tests',
                     'scripts']


def main(argv):
    try:
        no_show = len(argv) == 2 and argv[1] == '--no-show'

        os.chdir(WORKING_DIR)

        print("Generating API docs...")
        for module in MODULES_TO_APIDOC:
            run_apidoc(module)

        os.chdir(DOCS_ROOT)

        print("Cleaning docs with '{}':".format(COMMAND_CLEAN_DOCS))
        sub.check_call(COMMAND_CLEAN_DOCS, shell=True)

        print("Building docs with '{}':".format(COMMAND_BUILD_DOCS))
        # SPHINXBUILD environment variable is for Windows make.bat
        os.environ['SPHINXBUILD'] = SPHINXBUILD
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

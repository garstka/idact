#!/usr/bin/env python3
"""Generates diagrams using pyreverse and graphviz."""

import os
import pathlib
import subprocess as sub
import sys

COMMAND_GENERATE_DIAGRAM = ("pyreverse"
                            " --output dot"
                            " --project idact"
                            " --show-ancestors 2"
                            " --all-associated"
                            " --filter-mode SPECIAL"
                            " {path}")

COMMAND_CONVERT_TO_PNG = ("dot"
                          " -Tpng"
                          " -o {out_path}"
                          " classes_idact.dot")

DIAGRAMS_TO_GENERATE = {"core": "idact/core",
                        "detail-core": " idact/detail/nodes"
                                       " idact/detail/cluster_impl.py",
                        "detail-allocation": "idact/detail/allocation"
                                             " idact/detail/slurm",
                        "detail-config": "idact/detail/config",
                        "detail-other": "idact/detail/auth"
                                        " idact/detail/environment"
                                        " idact/detail/helper"
                                        " idact/cli.py"}

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

OUTPUT_DIR = os.path.join(WORKING_DIR, 'docs/diagrams')


def main():
    try:
        os.chdir(WORKING_DIR)

        pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        print("Generating diagrams...")

        for diagram_name, path in DIAGRAMS_TO_GENERATE.items():
            print("Generating diagram: {diagram_name}".format(
                diagram_name=diagram_name))
            sub.check_call(
                COMMAND_GENERATE_DIAGRAM.format(
                    path=path),
                shell=True)
            sub.check_call(
                COMMAND_CONVERT_TO_PNG.format(
                    out_path=os.path.join(OUTPUT_DIR,
                                          "{diagram_name}.png".format(
                                              diagram_name=diagram_name))),
                shell=True)

        return 0
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())

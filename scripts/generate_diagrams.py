#!/usr/bin/env python3
"""Generates diagrams using `pyreverse` and `graphviz`."""

import os
import pathlib
import subprocess as sub
import sys

PYREVERSE = ('{python} -c'
             ' "from pylint import run_pyreverse;'
             ' run_pyreverse()"').format(python=sys.executable)

COMMAND_GENERATE_DIAGRAM = ("{pyreverse}"
                            " --output dot"
                            " --project idact"
                            " --show-ancestors 2"
                            " --all-associated"
                            " --filter-mode SPECIAL"
                            " {{path}}".format(pyreverse=PYREVERSE))

COMMAND_CONVERT_TO_PNG = ("dot"
                          " -Tpng"
                          " -o {out_path}"
                          " classes_idact.dot")

DIAGRAMS_TO_GENERATE = {
    "core-nodes": " idact/core/cluster.py"
                  " idact/core/node.py"
                  " idact/core/node_resource_status.py"
                  " idact/core/nodes.py"
                  " idact/core/walltime.py",
    "core-deployments": " idact/core/dask_deployment.py"
                        " idact/core/jupyter_deployment.py"
                        " idact/core/synchronized_deployments.py"
                        " idact/core/tunnel.py",
    "core-config-tunnels": " idact/core/config.py"
                           " idact/core/tunnel.py",
    "detail-core-nodes":
        " idact/detail/nodes"
        " idact/detail/cluster_impl.py",
    "detail-core-deployments":
        " idact/detail/dask/dask_deployment_impl.py"
        " idact/detail/dask/dask_diagnostics_impl.py"
        " idact/detail/jupyter/jupyter_deployment_impl.py"
        " idact/detail/deployment_sync/synchronized_deployments_impl.py",
    "detail-core-tunnels":
        " idact/detail/tunnel/first_hop_tunnel.py"
        " idact/detail/tunnel/multi_hop_tunnel.py"
        " idact/detail/tunnel/ssh_tunnel.py"
        " idact/detail/tunnel/tunnel_internal.py",
    "detail-core-config":
        " idact/detail/config/client/client_cluster_config.py"
        " idact/detail/config/client/setup_actions_config.py"
        " idact/detail/config/client/retry_config_impl.py",
    "detail-allocation": "idact/detail/allocation"
                         " idact/detail/slurm",
    "detail-config": "idact/detail/config/client/client_config.py",
    "detail-deployment": "idact/detail/dask/dask_scheduler_deployment.py"
                         " idact/detail/dask/dask_worker_deployment.py"
                         " idact/detail/deployment"
                         " idact/detail/entry_point",
    "detail-deployment-sync": "idact/detail/deployment_sync"
                              "/deployment_definition.py"
                              " idact/detail/deployment_sync"
                              "/deployment_definitions.py",
    "detail-other": "idact/detail/auth"
                    " idact/detail/environment"
                    " idact/detail/helper"
                    " idact/detail/log/debug_log_filter.py"
                    " idact/detail/serialization/serializable.py"
                    " idact/detail/tunnel/binding.py"}

WORKING_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

OUTPUT_DIR = os.path.join(WORKING_DIR, 'docs/diagrams')


def main():
    """Main script function."""
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

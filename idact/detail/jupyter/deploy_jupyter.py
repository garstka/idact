"""This module contains a function for deploying Jupyter notebook."""

import json

import fabric.decorators
from fabric.context_managers import cd
from fabric.operations import run

from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.deployment.create_deployment_dir import create_runtime_dir
from idact.detail.deployment.deploy_generic import deploy_generic
from idact.detail.deployment.get_deployment_script_contents import \
    get_deployment_script_contents
from idact.detail.helper.get_free_remote_port import get_free_remote_port
from idact.detail.helper.get_remote_file import get_remote_file
from idact.detail.helper.retry import retry
from idact.detail.helper.stage_info import stage_debug
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal


def deploy_jupyter(node: NodeInternal, local_port: int) -> JupyterDeployment:
    """Deploys a Jupyter Notebook server on the node, and creates a tunnel
        to a local port.

        :param node: Node to deploy Jupyter Notebook on.

        :param local_port: Local tunnel binding port.

    """
    log = get_logger(__name__)

    with stage_debug(log, "Creating a runtime dir."):
        runtime_dir = create_runtime_dir(node=node)

    with stage_debug(log, "Obtaining a free remote port."):
        remote_port = get_free_remote_port(node=node)

    deployment_commands = []
    deployment_commands.append(
        'export JUPYTER_RUNTIME_DIR="{runtime_dir}"'.format(
            runtime_dir=runtime_dir))

    deployment_commands.append(
        'jupyter notebook'
        ' --ip 0.0.0.0'
        ' --port "{remote_port}"'
        ' --no-browser'.format(remote_port=remote_port))

    script_contents = get_deployment_script_contents(
        deployment_commands=deployment_commands,
        setup_actions=node.config.setup_actions.jupyter)

    log.debug("Deployment script contents: %s", script_contents)
    with stage_debug(log, "Deploying script."):
        deployment = deploy_generic(node=node,
                                    script_contents=script_contents,
                                    capture_output_seconds=5,
                                    runtime_dir=runtime_dir)

    with cancel_on_failure(deployment):
        @fabric.decorators.task
        def load_nbserver_json():
            """Loads notebook parameters from a json file."""
            with cd(runtime_dir):
                nbserver_json_path = run("realpath $PWD/nbserver-*.json") \
                    .splitlines()[0]
            run("cat '{nbserver_json_path}' > /dev/null".format(
                nbserver_json_path=nbserver_json_path))
            nbserver_json_str = get_remote_file(nbserver_json_path)
            nbserver_json = json.loads(nbserver_json_str)
            return int(nbserver_json['port']), nbserver_json['token']

        with stage_debug(log, "Obtaining info about notebook from json file."):
            actual_port, token = retry(
                lambda: node.run_task(task=load_nbserver_json),
                retries=5,
                seconds_between_retries=3)

        with stage_debug(log, "Opening a tunnel to notebook."):
            tunnel = node.tunnel(there=actual_port,
                                 here=local_port)

        return JupyterDeploymentImpl(node=node,
                                     deployment=deployment,
                                     tunnel=tunnel,
                                     token=token)

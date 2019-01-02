"""This module contains a function for deploying Jupyter notebook."""

import json

import fabric.decorators
from fabric.context_managers import cd
from fabric.operations import run

from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.retry import Retry
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.deployment.create_deployment_dir import create_runtime_dir
from idact.detail.deployment.create_log_file import create_log_file
from idact.detail.deployment.deploy_generic import deploy_generic

from idact.detail.deployment.get_command_to_append_local_bin import \
    get_command_to_append_local_bin
from idact.detail.deployment.get_deployment_script_contents import \
    get_deployment_script_contents
from idact.detail.helper.get_free_remote_port import get_free_remote_port
from idact.detail.helper.get_remote_file import get_remote_file
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_debug
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
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

    if node.config.use_jupyter_lab:
        jupyter_version = 'lab'
    else:
        jupyter_version = 'notebook'

    deployment_commands = [
        'export JUPYTER_RUNTIME_DIR="{runtime_dir}"'.format(
            runtime_dir=runtime_dir),
        get_command_to_append_local_bin()]

    log_file = create_log_file(node=node, runtime_dir=runtime_dir)

    deployment_commands.append(
        'jupyter {jupyter_version}'
        ' --ip 127.0.0.1'
        ' --port "{remote_port}"'
        ' --no-browser > {log_file} 2>&1'.format(
            jupyter_version=jupyter_version,
            remote_port=remote_port,
            log_file=log_file))

    script_contents = get_deployment_script_contents(
        deployment_commands=deployment_commands,
        setup_actions=node.config.setup_actions.jupyter)

    log.debug("Deployment script contents: %s", script_contents)
    with stage_debug(log, "Deploying script."):
        deployment = deploy_generic(node=node,
                                    script_contents=script_contents,
                                    runtime_dir=runtime_dir)

    with cancel_on_failure(deployment):
        @fabric.decorators.task
        def load_nbserver_json():
            """Loads notebook parameters from a json file."""
            with capture_fabric_output_to_log():
                with cd(runtime_dir):
                    nbserver_json_path = run(
                        "readlink -vf $PWD/nbserver-*.json").splitlines()[0]
                run("cat '{log_file}' || exit 0".format(
                    log_file=log_file))
                run("cat '{nbserver_json_path}' > /dev/null".format(
                    nbserver_json_path=nbserver_json_path))
                nbserver_json_str = get_remote_file(nbserver_json_path)
                nbserver_json = json.loads(nbserver_json_str)
                return int(nbserver_json['port']), nbserver_json['token']

        with stage_debug(log, "Obtaining info about notebook from json file."):
            actual_port, token = retry_with_config(
                lambda: node.run_task(task=load_nbserver_json),
                name=Retry.JUPYTER_JSON,
                config=node.config)

        with stage_debug(log, "Opening a tunnel to notebook."):
            tunnel = node.tunnel(there=actual_port,
                                 here=local_port)

        return JupyterDeploymentImpl(deployment=deployment,
                                     tunnel=tunnel,
                                     token=token)

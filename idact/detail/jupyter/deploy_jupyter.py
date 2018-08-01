import json

import fabric.decorators
from fabric.context_managers import cd
from fabric.operations import run

from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.deployment.deploy_generic import deploy_generic
from idact.detail.deployment.deployment_properties import \
    DEPLOYMENT_ID_LENGTH, DEPLOYMENT_RUNTIME_DIR_FORMAT
from idact.detail.helper.get_free_remote_port import get_free_remote_port
from idact.detail.helper.get_random_file_name import get_random_file_name
from idact.detail.helper.get_remote_file import get_remote_file
from idact.detail.helper.retry import retry
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.detail.nodes.node_internal import NodeInternal


def deploy_jupyter(node: NodeInternal, local_port: int) -> JupyterDeployment:
    """Deploys a Jupyter Hub server on the node, and creates a tunnel
       to local_port.

        :param node: Node to deploy Jupyter on.

        :param local_port: Local tunnel binding port.
    """
    deployment_id = get_random_file_name(length=DEPLOYMENT_ID_LENGTH)
    formatted_runtime_dir = DEPLOYMENT_RUNTIME_DIR_FORMAT.format(
        deployment_id=deployment_id)

    node.run('mkdir -p {}'.format(formatted_runtime_dir))
    runtime_dir = node.run("realpath {}".format(formatted_runtime_dir))

    remote_port = get_free_remote_port(node=node)
    command = ('export JUPYTER_RUNTIME_DIR="{runtime_dir}"'
               ' && jupyter notebook'
               ' --ip 0.0.0.0'
               ' --port "{remote_port}"'
               ' --no-browser').format(runtime_dir=runtime_dir,
                                       remote_port=remote_port)
    deployment = deploy_generic(node=node,
                                command=command,
                                capture_output_seconds=5)

    @fabric.decorators.task
    def load_nbserver_json():
        with cd(runtime_dir):
            nbserver_json_path = run("echo $PWD/nbserver-*.json")
            nbserver_json_str = get_remote_file(nbserver_json_path)
            nbserver_json = json.loads(nbserver_json_str)
            return int(nbserver_json['port']), nbserver_json['token']

    access_node = node
    actual_port, token = retry(
        lambda: access_node.run_task(task=load_nbserver_json),
        retries=5,
        seconds_between_retries=3)

    tunnel = node.tunnel(there=actual_port,
                         here=local_port)

    return JupyterDeploymentImpl(node=node,
                                 deployment=deployment,
                                 tunnel=tunnel,
                                 token=token,
                                 runtime_dir=runtime_dir)

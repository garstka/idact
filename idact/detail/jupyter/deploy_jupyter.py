import logging

from idact.core.nodes import Node
from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl

JUPYTER_REMOTE_PORT = 8090


def deploy_jupyter(node: Node, local_port: int) -> JupyterDeployment:
    """Deploys a Jupyter Hub server on the node, and creates a tunnel
       to local_port.

        :param node: Node to deploy Jupyter on.

        :param local_port: Local tunnel binding port.
    """
    try:
        node.run("nohup jupyterhub"
                 " --ip 0.0.0.0"
                 " --port {remote_port}"
                 " --no-db &".format(remote_port=JUPYTER_REMOTE_PORT),
                 timeout=1)
    except TimeoutError as e:
        logging.info(e)

    tunnel = node.tunnel(there=JUPYTER_REMOTE_PORT,
                         here=local_port)

    return JupyterDeploymentImpl(node=node,
                                 tunnel=tunnel)

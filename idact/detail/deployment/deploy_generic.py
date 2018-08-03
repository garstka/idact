from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.deployment.get_deployment_command import \
    get_deployment_command
from idact.detail.entry_point.upload_entry_point import upload_entry_point
from idact.detail.nodes.node_internal import NodeInternal


def deploy_generic(node: NodeInternal,
                   script_contents: str,
                   capture_output_seconds: int) -> GenericDeployment:
    """Deploys a program on the node.

        :param node: Node to deploy the program on.

        :param script_contents: Deployment script contents.

        :param capture_output_seconds: Seconds to wait for command output.
    """

    script_path = upload_entry_point(contents=script_contents,
                                     node=node)
    output = node.run(get_deployment_command(
        script_path=script_path,
        capture_output_seconds=capture_output_seconds))
    lines = output.splitlines()
    pid = int(lines[0])
    return GenericDeployment(node=node,
                             pid=pid,
                             output='\n'.join(lines[1:]))

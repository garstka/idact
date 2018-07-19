from idact.core.nodes import Node
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.deployment.get_deployment_command import \
    get_deployment_command


def deploy_generic(node: Node,
                   command: str,
                   capture_output_seconds: int) -> GenericDeployment:
    """Deploys a program on the node.

        :param node: Node to deploy the program on.

        :param command: Command to run the program.

        :param capture_output_seconds: Seconds to wait for command output.
    """

    output = node.run(get_deployment_command(
        command=command,
        capture_output_seconds=capture_output_seconds))
    lines = output.splitlines()
    pid = int(lines[0])
    return GenericDeployment(node=node,
                             pid=pid,
                             output='\n'.join(lines[1:]))

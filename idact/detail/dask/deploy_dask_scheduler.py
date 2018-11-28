"""This module contains functionality for deploying a Dask scheduler."""

import re
from contextlib import ExitStack

import fabric.decorators

from idact.core.retry import Retry
from idact.detail.dask.create_scratch_dir import create_scratch_subdir
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.dask.get_scheduler_deployment_script import \
    get_scheduler_deployment_script
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.deployment.create_deployment_dir import create_runtime_dir
from idact.detail.deployment.create_log_file import create_log_file
from idact.detail.deployment.deploy_generic import deploy_generic
from idact.detail.helper.get_free_remote_port import get_free_remote_ports
from idact.detail.helper.get_remote_file import get_remote_file
from idact.detail.helper.remove_runtime_dir \
    import remove_runtime_dir_on_failure
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.tunnel.close_tunnel_on_failure import close_tunnel_on_failure

SCHEDULER_AT_REGEX = r"Scheduler at:\s+?([^\s]+)$"
__SCHEDULER_AT_REGEX_COMPILED = re.compile(SCHEDULER_AT_REGEX,
                                           re.MULTILINE)


def extract_address_from_output(output: str) -> str:
    """Extracts scheduler address from Dask scheduler output.

        :param output: Dask scheduler output.
    """

    match = __SCHEDULER_AT_REGEX_COMPILED.search(output)
    if not match:
        raise ValueError("Unable to determine scheduler address.")

    return match.groups()[0]


def deploy_dask_scheduler(node: NodeInternal) -> DaskSchedulerDeployment:
    """Deploys a Dask scheduler on the node.

        :param node: Node to deploy on.

    """
    log = get_logger(__name__)

    with ExitStack() as stack:
        with stage_debug(log, "Creating a runtime dir."):
            runtime_dir = create_runtime_dir(node=node)
            stack.enter_context(
                remove_runtime_dir_on_failure(node=node,
                                              runtime_dir=runtime_dir))

        with stage_debug(log, "Obtaining free remote ports."):
            remote_port, bokeh_port = get_free_remote_ports(count=2, node=node)

        with stage_debug(log, "Creating a scratch subdirectory."):
            scratch_subdir = create_scratch_subdir(node=node)

        log_file = create_log_file(node=node, runtime_dir=runtime_dir)

        script_contents = get_scheduler_deployment_script(
            remote_port=remote_port,
            bokeh_port=bokeh_port,
            scratch_subdir=scratch_subdir,
            log_file=log_file,
            config=node.config)

        log.debug("Deployment script contents: %s", script_contents)

        with stage_debug(log, "Deploying script."):
            deployment = deploy_generic(node=node,
                                        script_contents=script_contents,
                                        runtime_dir=runtime_dir)
            stack.enter_context(cancel_on_failure(deployment))

        @fabric.decorators.task
        def extract_address_from_log() -> str:
            """Extracts scheduler address from a log file."""
            with capture_fabric_output_to_log():
                output = get_remote_file(remote_path=log_file)
            log.debug("Log file: %s", output)
            return extract_address_from_output(output=output)

        with stage_debug(log, "Obtaining scheduler address."):
            address = retry_with_config(
                lambda: node.run_task(task=extract_address_from_log),
                name=Retry.GET_SCHEDULER_ADDRESS,
                config=node.config)

        with stage_debug(log, "Opening a tunnel to scheduler."):
            tunnel = node.tunnel(here=remote_port, there=remote_port)
            stack.enter_context(close_tunnel_on_failure(tunnel))
            log.debug("Scheduler local port: %d", tunnel.here)

        with stage_debug(log, "Opening a tunnel to bokeh diagnostics server."):
            bokeh_tunnel = node.tunnel(here=bokeh_port, there=bokeh_port)
            stack.enter_context(close_tunnel_on_failure(bokeh_tunnel))
            log.debug("Diagnostics local port: %d", bokeh_tunnel.here)

        return DaskSchedulerDeployment(deployment=deployment,
                                       tunnel=tunnel,
                                       bokeh_tunnel=bokeh_tunnel,
                                       address=address)

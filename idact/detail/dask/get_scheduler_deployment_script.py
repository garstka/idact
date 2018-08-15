import shlex

from idact.core.config import ClusterConfig
from idact.detail.deployment.get_deployment_script_contents import \
    get_deployment_script_contents


def get_scheduler_deployment_script(remote_port: int,
                                    bokeh_port: int,
                                    scratch_subdir: str,
                                    log_file: str,
                                    config: ClusterConfig) -> str:
    """Returns the deployment script for dask scheduler.

        :param remote_port:    Scheduler port.
        :param bokeh_port:     Bokeh diagnostics server port.
        :param scratch_subdir: Scratch directory.
        :param log_file:       Log file path.
        :param config:         Cluster config.

    """
    deployment_commands = [
        'dask-scheduler'
        ' --host 0.0.0.0'
        ' --port {remote_port}'
        ' --bokeh'
        ' --bokeh-port {bokeh_port}'
        ' --no-show'
        ' --local-directory {scratch_subdir}'
        ' > {log_file} 2>&1'.format(
            remote_port=remote_port,
            bokeh_port=bokeh_port,
            scratch_subdir=shlex.quote(scratch_subdir),
            log_file=log_file)]

    script_contents = get_deployment_script_contents(
        deployment_commands=deployment_commands,
        setup_actions=config.setup_actions.dask)
    return script_contents

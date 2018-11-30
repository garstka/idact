"""This module contains a function for generating a Dask scheduler deployment
    script."""

import shlex
import bitmath

from idact.core.config import ClusterConfig
from idact.detail.deployment.get_command_to_append_local_bin import \
    get_command_to_append_local_bin
from idact.detail.deployment.get_deployment_script_contents import \
    get_deployment_script_contents


def get_worker_deployment_script(scheduler_address: str,
                                 bokeh_port: int,
                                 scratch_subdir: str,
                                 log_file: str,
                                 cores: int,
                                 memory_limit: bitmath.Byte,
                                 config: ClusterConfig) -> str:
    """Returns the deployment script for dask worker.

        :param scheduler_address: Scheduler address.
        :param bokeh_port:        Bokeh diagnostics server port.
        :param scratch_subdir:    Scratch directory.
        :param log_file:          Log file path.
        :param cores:             Node core count / worker thread count.
        :param memory_limit:      Node allocated memory / worker memory limit.
        :param config:            Cluster config.

    """
    deployment_commands = [
        get_command_to_append_local_bin(),
        'dask-worker'
        ' {scheduler_address}'
        ' --host 0.0.0.0'
        ' --bokeh'
        ' --bokeh-port {bokeh_port}'
        ' --nanny'
        ' --reconnect'
        ' --nprocs 1'
        ' --nthreads {cores}'
        ' --memory-limit {bytes}'
        ' --local-directory {scratch_subdir}'
        ' > {log_file} 2>&1'.format(
            scheduler_address=shlex.quote(scheduler_address),
            bokeh_port=bokeh_port,
            cores=cores,
            bytes=memory_limit.bytes,
            scratch_subdir=shlex.quote(scratch_subdir),
            log_file=log_file)]

    script_contents = get_deployment_script_contents(
        deployment_commands=deployment_commands,
        setup_actions=config.setup_actions.dask)
    return script_contents

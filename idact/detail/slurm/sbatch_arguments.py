"""This module contains functionality for preparing sbatch arguments."""

from typing import Dict, Optional

from idact.detail.allocation.allocation_parameters import AllocationParameters


def sbatch_set_nodes(params: AllocationParameters,
                     args: Dict[str, str]):
    """Sets the node count.

        :param params: Allocation params.

        :param args: Arguments to modify.
    """
    args['--nodes'] = str(params.nodes)


def sbatch_set_cores(params: AllocationParameters,
                     args: Dict[str, str]):
    """Sets the core count by setting `cpus-per-task`.
        A single task is run per node, which makes this parameter in control
        of the core count.

        :param params: Allocation params.

        :param args: Arguments to modify.
    """
    args['--cpus-per-task'] = str(params.cores)


def sbatch_set_memory_per_node(params: AllocationParameters,
                               args: Dict[str, str]):
    """Sets the memory per node.

        Max resolution is K (kilobytes, assuming kibibytes)

        :param params: Allocation params.

        :param args: Arguments to modify.
    """
    args['--mem'] = '{}K'.format(int(params.memory_per_node.to_KiB()))


def sbatch_set_walltime(params: AllocationParameters,
                        args: Dict[str, str]):
    """Sets the job walltime.

        :param params: Allocation params.

        :param args: Arguments to modify.
    """
    walltime = params.walltime
    args['--time'] = '{}-{:02d}:{:02d}:{:02d}'.format(
        walltime.days,
        walltime.hours,
        walltime.minutes,
        walltime.seconds)


class SbatchArguments:
    """Prepares arguments for running Slurm `sbatch` command.

       :param params: Generic allocation parameters.

    """

    ALLOWED_PARAMS = {'nodes': sbatch_set_nodes,
                      'cores': sbatch_set_cores,
                      'memory_per_node': sbatch_set_memory_per_node,
                      'walltime': sbatch_set_walltime}
    """Map of allowed :class:`.AllocationParams` members to handlers for adding
       command line arguments."""

    REQUIRED_PARAMS = {'nodes',
                       'cores',
                       'memory_per_node',
                       'walltime'}
    """Members of :class:`.AllocationParams` that must be specified."""

    def __init__(self,
                 params: AllocationParameters):

        self._native_args = {arg: value
                             for arg, value
                             in params.native_args.items()}

        self._args = {}
        for param, value in params.all.items():
            try:
                handler = self.ALLOWED_PARAMS[param]
            except KeyError as e:
                raise ValueError("Slurm: "
                                 "Unsupported parameter: "
                                 "'{}'".format(param)) from e
            if value is None and param in self.REQUIRED_PARAMS:
                raise ValueError("Slurm: "
                                 "Required parameter missing: "
                                 "'{}'".format(param))
            handler(params=params, args=self._args)

    @property
    def native_args(self) -> Dict[str, Optional[str]]:
        """Native sbatch arguments."""
        return self._native_args

    @property
    def args(self) -> Dict[str, Optional[str]]:
        """Supported sbatch arguments."""
        return self._args

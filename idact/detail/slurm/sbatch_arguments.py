from typing import Dict, Optional

from idact.detail.allocation.allocation_parameters import AllocationParameters


def sbatch_set_nodes(params: AllocationParameters,
                     args: Dict[str, str]):
    args['--nodes'] = str(params.nodes)


def sbatch_set_cores(params: AllocationParameters,
                     args: Dict[str, str]):
    args['--cpus-per-task'] = str(params.cores)


def sbatch_set_memory_per_node(params: AllocationParameters,
                               args: Dict[str, str]):
    # Max resolution is K (kilobytes, assuming kibibytes)
    args['--mem'] = '{}K'.format(int(params.memory_per_node.to_KiB()))


def sbatch_set_walltime(params: AllocationParameters,
                        args: Dict[str, str]):
    walltime = params.walltime
    args['--time'] = '{}-{:02d}:{:02d}:{:02d}'.format(
        walltime.days,
        walltime.hours,
        walltime.minutes,
        walltime.seconds)


class SbatchArguments:
    """Prepares arguments for running SLURM sbatch command.

       :param params: Generic allocation parameters."""

    ALLOWED_PARAMS = {'nodes': sbatch_set_nodes,
                      'cores': sbatch_set_cores,
                      'memory_per_node': sbatch_set_memory_per_node,
                      'walltime': sbatch_set_walltime}
    """Map of allowed :class:`AllocationParams` members to handlers for adding
       command line arguments."""

    REQUIRED_PARAMS = {'nodes',
                       'cores',
                       'memory_per_node',
                       'walltime'}
    """Members of :class:`AllocationParams` that must be specified."""

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
                raise ValueError("SLURM: "
                                 "Unsupported parameter: "
                                 "'{}'".format(param)) from e
            if value is None and param in self.REQUIRED_PARAMS:
                raise ValueError("SLURM: "
                                 "Required parameter missing: "
                                 "'{}'".format(param))
            handler(params=params, args=self._args)

    @property
    def native_args(self) -> Dict[str, Optional[str]]:
        return self._native_args

    @property
    def args(self) -> Dict[str, Optional[str]]:
        return self._args

"""This module contains the implementation of the Dask deployment interface."""

from contextlib import ExitStack

from typing import List

import dask.distributed

from idact.core.dask_deployment import DaskDeployment, DaskDiagnostics
from idact.detail.dask.dask_diagnostics_impl import DaskDiagnosticsImpl
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.deployment.cancel_on_exit import cancel_on_exit


class DaskDeploymentImpl(DaskDeployment):
    """Implementation of :class:`DaskDeployment`.

        :param scheduler: Scheduler deployment.

        :param workers: Worker deployments.

    """

    def __init__(self,
                 scheduler: DaskSchedulerDeployment,
                 workers: List[DaskWorkerDeployment]):
        self._scheduler = scheduler
        self._workers = workers

        tunnels = [self._scheduler.bokeh_tunnel]
        tunnels.extend([worker.bokeh_tunnel for worker in workers])
        self._diagnostics = DaskDiagnosticsImpl(tunnels=tunnels)

    def get_client(self) -> dask.distributed.Client:
        return dask.distributed.Client(address=self._scheduler.local_address)

    @property
    def diagnostics(self) -> DaskDiagnostics:
        return self._diagnostics

    def cancel(self):
        with ExitStack() as stack:
            stack.enter_context(cancel_on_exit(self._scheduler))
            for worker in self._workers:
                stack.enter_context(cancel_on_exit(worker))

    def __str__(self):
        return \
            ("DaskDeployment(scheduler={local_address}/{address}, "
             "workers={worker_count}"
             ")").format(local_address=self._scheduler.local_address,
                         address=self._scheduler.address,
                         worker_count=len(self._workers))

    def __repr__(self):
        return str(self)

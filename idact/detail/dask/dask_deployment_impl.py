"""This module contains the implementation of the Dask deployment interface."""

from contextlib import ExitStack

from typing import List, Optional

import dask.distributed

from idact.core.config import ClusterConfig
from idact.core.dask_deployment import DaskDeployment, DaskDiagnostics
from idact.detail.dask.dask_diagnostics_impl import DaskDiagnosticsImpl
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.deployment.cancel_on_exit import cancel_on_exit, \
    cancel_local_on_exit
from idact.detail.helper.get_uuid import get_uuid
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes


class DaskDeploymentImpl(DaskDeployment, Serializable):
    """Implementation of :class:`DaskDeployment`.

        :param scheduler: Scheduler deployment.

        :param workers: Worker deployments.

        :param uuid: Unique deployment identifier.

    """

    def __init__(self,
                 scheduler: DaskSchedulerDeployment,
                 workers: List[DaskWorkerDeployment],
                 uuid: Optional[str] = None):
        self._scheduler = scheduler
        self._workers = workers

        self._diagnostics = DaskDiagnosticsImpl(
            scheduler_tunnel=self._scheduler.bokeh_tunnel,
            worker_tunnels=[worker.bokeh_tunnel for worker in workers])

        self._uuid = uuid if uuid is not None else get_uuid()

    def get_client(self) -> dask.distributed.Client:
        return dask.distributed.Client(address=self._scheduler.local_address)

    @property
    def diagnostics(self) -> DaskDiagnostics:
        return self._diagnostics

    @property
    def scheduler(self) -> DaskSchedulerDeployment:
        """Scheduler deployment."""
        return self._scheduler

    def cancel(self):
        with ExitStack() as stack:
            stack.enter_context(cancel_on_exit(self._scheduler))
            for worker in self._workers:
                stack.enter_context(cancel_on_exit(worker))

    def cancel_local(self):
        with ExitStack() as stack:
            stack.enter_context(cancel_local_on_exit(self._scheduler))
            for worker in self._workers:
                stack.enter_context(cancel_local_on_exit(worker))

    def __str__(self):
        return \
            ("DaskDeployment(scheduler={local_address}/{address}, "
             "workers={worker_count}"
             ")").format(local_address=self._scheduler.local_address,
                         address=self._scheduler.address,
                         worker_count=len(self._workers))

    def __repr__(self):
        return str(self)

    @property
    def uuid(self) -> str:
        """Unique deployment id."""
        return self._uuid

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DASK_DEPLOYMENT_IMPL),
                'scheduler': self._scheduler.serialize(),
                'workers': [worker.serialize()
                            for worker in self._workers]}

    @staticmethod
    def deserialize(config: ClusterConfig,
                    uuid: str,
                    serialized: dict) -> 'DaskDeploymentImpl':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DASK_DEPLOYMENT_IMPL)

            scheduler = DaskSchedulerDeployment.deserialize(
                config=config,
                serialized=serialized['scheduler'])
            workers = [
                DaskWorkerDeployment.deserialize(
                    config=config,
                    serialized=serialized_worker)
                for serialized_worker in serialized['workers']]

            return DaskDeploymentImpl(scheduler=scheduler,
                                      workers=workers,
                                      uuid=uuid)
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

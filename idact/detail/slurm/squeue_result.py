"""This module contains the implementation of a data class for an squeue
    result."""

import datetime
from typing import Optional, List


class SqueueResult:
    """A row extracted from the output of `squeue`.

        :param job_id:     Unique job id.
                           Corresponds to the `%A` format parameter.

        :param end_time:   Expected UTC job end time.
                           `None` for a running job means no limit.
                           Based on the time limit: `%L` format parameter.

        :param node_count: Count of the allocated nodes.
                           Corresponds to the `%D` format parameter.

        :param node_list:  List of the allocated nodes.
                           Corresponds to the `%R` format parameter.

        :param reason:     Reason for the current job state.
                           Corresponds to the `%r` format parameter.

        :param state:      Long job state code, e.g. `RUNNING`, `PENDING`.
                           Corresponds to the `%T` format parameter.

    """

    def __init__(self,
                 job_id: int,
                 end_time: Optional[datetime.datetime],
                 node_count: int,
                 node_list: Optional[List[str]],
                 reason: Optional[str],
                 state: str):
        self._job_id = job_id
        self._end_time = end_time
        self._node_count = node_count
        self._node_list = node_list
        self._reason = reason
        self._state = state

    @property
    def job_id(self) -> int:
        """Job id."""
        return self._job_id

    @property
    def end_time(self) -> Optional[datetime.datetime]:
        """Expected job end time."""
        return self._end_time

    @property
    def node_count(self) -> int:
        """Allocated node count."""
        return self._node_count

    @property
    def node_list(self) -> Optional[List[str]]:
        """Allocated node list."""
        return self._node_list

    @property
    def reason(self) -> Optional[str]:
        """Reason for the current job state."""
        return self._reason

    @property
    def state(self) -> str:
        """Job state code."""
        return self._state

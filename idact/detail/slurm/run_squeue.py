"""This module contains functionality for running squeue on a node."""

import datetime
import shlex
from typing import Dict, Optional, List

from idact.core.nodes import Node
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.helper.utc_now import utc_now
from idact.detail.log.get_logger import get_logger
from idact.detail.slurm.squeue_result import SqueueResult


# pylint: disable=invalid-name


def extract_squeue_format_A(value: str) -> int:
    """Extracts the job id `%A` from `squeue` output.

        :param value: Job id as string.
    """
    return int(value)


def extract_squeue_format_D(value: str) -> int:
    """Extracts the node count `%D` from `squeue` output.

        :param value: Node count as string.
    """
    return int(value)


def extract_squeue_format_L(now: datetime.datetime,
                            value: str) -> Optional[datetime.datetime]:
    """Extracts time left `%L` from `squeue` output and returns finish time.

        :param now: Current time.

        :param value: Time left (days-hours:minutes:seconds).
    """
    if value in ['NOT_SET', 'UNLIMITED']:
        return None

    value = value.replace('-', ':')
    colons = value.count(':')
    if colons > 3:
        raise ValueError('Unexpected format.')
    value = '0:' * (3 - colons) + value
    days, hours, minutes, seconds = value.split(':')
    delta = datetime.timedelta(days=int(days),
                               hours=int(hours),
                               minutes=int(minutes),
                               seconds=int(seconds))
    return now + delta


def extract_squeue_format_r(value: str) -> Optional[str]:
    """Extracts the job reason code `%r` from `squeue` output.

        :param value: Job reason code.
    """
    if value == 'None':
        return None
    return value


def extract_squeue_format_R(value: str, node: Node) -> Optional[List[str]]:
    """Extracts the job node list `%R` from `squeue` output, and calls `scontrol`
        to extract each hostname.

        :param value: Job node list in a compact format, e.g. `node[1-7]`.

        :param node:  Node to call scontrol on.
    """
    if value.startswith('('):
        return None

    output = node.run("scontrol show hostname {}".format(shlex.quote(value)))
    hosts = [validate_hostname(i) for i in output.splitlines()]
    return hosts if hosts else None


def extract_squeue_format_T(value: str) -> str:
    """Extracts job state code `%T` from `squeue` output.

        :param: Job state code.
    """
    return value


def extract_squeue_line(now: datetime.datetime,
                        line: str,
                        node: Node) -> Optional[SqueueResult]:
    """Extracts information from `squeue` output line,
        where format is `%A|%D|%L|%r|%R|%T`.

        :param now: Current time for calculating job finish time.

        :param line: `squeue` output line.

        :param node: Node to run `scontrol` on.

    """
    if not line:
        return None
    components = line.split('|')

    try:
        job_id = extract_squeue_format_A(value=components[0])
        node_count = extract_squeue_format_D(value=components[1])
        end_time = extract_squeue_format_L(now=now, value=components[2])
        reason = extract_squeue_format_r(value=components[3])
        node_list = extract_squeue_format_R(value=components[4], node=node)
        state = extract_squeue_format_T(value=components[5])
    except ValueError:
        log = get_logger(__name__)
        log.debug("Exception", exc_info=1)
        return None

    return SqueueResult(job_id=job_id,
                        node_count=node_count,
                        end_time=end_time,
                        reason=reason,
                        node_list=node_list,
                        state=state)


def run_squeue(node: Node) -> Dict[int, SqueueResult]:
    """Runs `squeue` and extracts job statuses as results.

        :param node: Node to run `squeue` on.
    """

    now = utc_now()
    output = node.run("squeue --format '%A|%D|%L|%r|%R|%T'")
    lines = output.splitlines()[1:]  # Ignore header.
    results = {squeue_result.job_id: squeue_result
               for squeue_result
               in [extract_squeue_line(now=now,
                                       line=line,
                                       node=node)
                   for line in lines]
               if squeue_result is not None}

    return results

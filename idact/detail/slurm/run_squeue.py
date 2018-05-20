import datetime
import shlex
from typing import Dict, Optional, List

from idact.core.nodes import Node
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.helper.utc_now import utc_now
from idact.detail.slurm.squeue_result import SqueueResult


# pylint: disable=invalid-name


def extract_squeue_format_A(value: str) -> int:
    """Extracts the job id %A."""
    return int(value)


def extract_squeue_format_D(value: str) -> int:
    """Extracts the node count %D."""
    return int(value)


def extract_squeue_format_L(now: datetime.datetime,
                            value: str) -> Optional[datetime.datetime]:
    """Extracts time left %L: days-hours:minutes:seconds
       and adds it to now.
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
    """Extracts job reason code %r."""
    if value == 'None':
        return None
    return value


def extract_squeue_format_R(value: str, node: Node) -> Optional[List[str]]:
    """Extracts job node list %R."""
    if value.startswith('('):
        return None

    output = node.run("scontrol show hostname {}".format(shlex.quote(value)))
    hosts = [validate_hostname(i) for i in output.splitlines()]
    return hosts if hosts else None


def extract_squeue_format_T(value: str) -> str:
    """Extracts job state code %T."""
    return value


def extract_squeue_line(now: datetime.datetime,
                        line: str,
                        node: Node) -> Optional[SqueueResult]:
    """Extracts information from a squeue output line."""
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
        return None

    return SqueueResult(job_id=job_id,
                        node_count=node_count,
                        end_time=end_time,
                        reason=reason,
                        node_list=node_list,
                        state=state)


def run_squeue(node: Node) -> Dict[int, SqueueResult]:
    """Runs squeue on the given node."""

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

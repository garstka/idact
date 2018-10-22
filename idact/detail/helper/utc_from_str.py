"""This module contains a helper function for returning current datetime."""

import datetime
import dateutil.tz
import dateutil.parser


def utc_from_str(value: str) -> datetime.datetime:
    """Converts a string to an aware datetime object.

        :param value: UTC datetime from :meth:`datetime.isoformat`.

    """
    return dateutil.parser.isoparse(value).replace(
        tzinfo=dateutil.tz.tzutc())

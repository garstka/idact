"""This module contains a helper function for returning current datetime."""

import datetime
import dateutil.tz


def utc_now() -> datetime.datetime:
    """Returns an aware datetime object with current UTC datetime."""
    return datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())

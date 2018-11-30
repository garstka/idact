"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Walltime`.
"""

import re


class Walltime:
    """Simple job duration.

       :param days:    Must be greater or equal to 0.
       :param hours:   Must be in range [0,24).
       :param minutes: Must be in range [0,60).
       :param seconds: Must be in range [0,60).

       Walltime must not be zero.
    """

    WALLTIME_REGEX = r'^((\d+)-){0,1}(\d?\d):(\d\d):(\d\d)$'
    """Regular expression for a string that can be converted
       to a :class:`Walltime`
    """

    WALLTIME_REGEX_COMPILED = re.compile(WALLTIME_REGEX)

    def __init__(self,
                 days: int = 0,
                 hours: int = 0,
                 minutes: int = 0,
                 seconds: int = 0):

        if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            raise ValueError('Walltime of zero is not allowed.')
        if days < 0:
            raise ValueError('days parameter must be a non-negative integer.')
        if hours not in range(0, 24):
            raise ValueError('hours must be in range [0,24)')
        if minutes not in range(0, 60):
            raise ValueError('minutes must be in range [0,60)')
        if seconds not in range(0, 60):
            raise ValueError('seconds must be in range [0,60)')
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

    @property
    def days(self) -> int:
        """Number of days."""
        return self._days

    @property
    def hours(self) -> int:
        """Number of hours."""
        return self._hours

    @property
    def minutes(self) -> int:
        """Number of minutes."""
        return self._minutes

    @property
    def seconds(self) -> int:
        """Number of seconds."""
        return self._seconds

    @staticmethod
    def from_string(value: str) -> 'Walltime':
        """Creates a Walltime instance from a string.

           Accepted format: [days-]hours:minutes:seconds
           (see :const:`.Walltime.WALLTIME_REGEX`).

           :param value: String to parse.
        """
        match = Walltime.WALLTIME_REGEX_COMPILED.match(value)
        if not match:
            raise ValueError(
                "Could not create walltime from string: {}. "
                "Expected [days-]hours:minutes:seconds.".format(value))

        _, days, hours, minutes, seconds = match.groups()
        return Walltime(days=int(days) if days else 0,
                        hours=int(hours),
                        minutes=int(minutes),
                        seconds=int(seconds))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self._days != 0:
            days = "{days}-".format(days=self._days)
        else:
            days = ""
        return "{days}{hours:02d}:{minutes:02d}:{seconds:02d}".format(
            days=days,
            hours=self._hours,
            minutes=self._minutes,
            seconds=self._seconds)

    def __repr__(self):
        return str(self)

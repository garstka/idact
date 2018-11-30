from idact.core.config import RetryConfig

from idact.detail.config.validation.validate_non_negative_int import \
    validate_non_negative_int


class RetryConfigImpl(RetryConfig):
    """Implementation of retry config.

        :param count: Retry count.

        :param seconds_between: Seconds between retries.

    """

    def __init__(self, count: int, seconds_between: int):
        self._count = None
        self.count = validate_non_negative_int(count, 'count')

        self._seconds_between = None
        self.seconds_between = validate_non_negative_int(seconds_between,
                                                         'seconds_between')

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int):
        self._count = validate_non_negative_int(value, 'count')

    @property
    def seconds_between(self) -> int:
        return self._seconds_between

    @seconds_between.setter
    def seconds_between(self, value: int):
        self._seconds_between = validate_non_negative_int(value,
                                                          'seconds_between')

    def __str__(self):
        return (
            "RetryConfig(count={count},"
            " seconds_between={seconds_between})".format(
                count=self._count,
                seconds_between=self._seconds_between))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

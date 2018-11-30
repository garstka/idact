import logging


class DebugLogFilter(logging.Filter):
    """Sets every record's level to DEBUG."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno > logging.DEBUG:
            record.levelname = "DEBUG from {levelname}".format(
                levelname=record.levelname)
            record.levelno = logging.DEBUG
        return True

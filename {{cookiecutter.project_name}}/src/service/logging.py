import logging.config
from logging import Filter
from typing import Optional

from .config import config
from .middlewares.trace_id import correlation_id

from logging import LogRecord


def _trim_string(string: Optional[str], string_length: Optional[int]) -> Optional[str]:
    return string[:string_length] if string_length is not None and string else string


class CorrelationIdFilter(Filter):
    """Logging filter to attached correlation IDs to log records"""

    def __init__(self, name: str = '', uuid_length: Optional[int] = None, default_value: Optional[str] = None):
        super().__init__(name=name)
        self.uuid_length = uuid_length
        self.default_value = default_value

    def filter(self, record: 'LogRecord') -> bool:
        """
        Attach a correlation ID to the log record.

        Since the correlation ID is defined in the middleware layer, any
        log generated from a request after this point can easily be searched
        for, if the correlation ID is added to the message, or included as
        metadata.
        """
        cid = correlation_id.get(self.default_value)
        record.correlation_id = _trim_string(cid, self.uuid_length)
        return True


LOGGING_CONFIG = {
    'version': 1,
    'filters': {
        'request_id': {
            '()': CorrelationIdFilter,
        },
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:%(request_id)s\n%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': config.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            'filters': ['request_id'],
        },
    },
    'loggers': {
        config.APP_NAME: {
            'level': config.LOG_LEVEL,
            'handlers': (['console', ]),
        },
    },
    'disable_existing_loggers': False,
}


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

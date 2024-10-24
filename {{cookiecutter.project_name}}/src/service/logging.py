from logging import LogRecord
import logging.config

from .config import AppConfig
from .middlewares.correlation_id import CORRELATION_ID


class RequestIdFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:  # noqa: A003
        record.correlation_id = CORRELATION_ID.get()
        return True


def init_logging(config: AppConfig) -> None:
    LOGGING_CONFIG = {
        "version": 1,
        "filters": {"correlation_id": {"()": RequestIdFilter}},
        "formatters": {
            "default": {
                "format": "%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:%(correlation_id)s\n%(message)s\n",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "level": config.LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
                "filters": ["correlation_id"],
            }
        },
        "loggers": {config.APP_NAME: {"level": config.LOG_LEVEL, "handlers": (["console"])}},
        "disable_existing_loggers": False,
    }

    logging.config.dictConfig(LOGGING_CONFIG)

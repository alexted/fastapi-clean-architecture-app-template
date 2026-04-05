from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

from opentelemetry import trace
from pythonjsonlogger.json import JsonFormatter

from .middlewares.correlation_id import CORRELATION_ID

if TYPE_CHECKING:
    from .settings import AppConfig


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = CORRELATION_ID.get()

        span = trace.get_current_span()
        if span.is_recording():
            ctx = span.get_span_context()
            record.trace_id = format(ctx.trace_id, "032x")
            record.span_id = format(ctx.span_id, "016x")
        else:
            record.trace_id = None
            record.span_id = None

        return True


def init_logging(config: AppConfig) -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "filters": {"correlation_id": {"()": RequestIdFilter}},
            "formatters": {
                "default": {
                    "format": "%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:%(correlation_id)s\n%(message)s\n",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "json": {
                    "()": JsonFormatter,
                    "format": "%(levelname)s %(asctime)s %(name)s %(funcName)s %(correlation_id)s %(trace_id)s %(span_id)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "json_ensure_ascii": False,
                },
            },
            "handlers": {
                "console": {
                    "level": config.LOG_LEVEL,
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": sys.stdout,
                    "filters": ["correlation_id"],
                }
            },
            "loggers": {
                config.APP_NAME: {"level": config.LOG_LEVEL, "handlers": (["console"])},
                "granian": {"level": "INFO", "handlers": ["console"], "propagate": False},
                "granian.access": {"level": "WARNING", "handlers": ["console"]},
                "granian.error": {"level": "ERROR", "handlers": ["console"]},
                "fastapi": {"level": "WARNING", "handlers": ["console"]},
                "sqlalchemy.engine": {"level": "INFO", "handlers": ["console"]},
                "alembic": {"level": "INFO", "handlers": ["console"]},
                "httpx": {"level": "WARNING", "handlers": ["console"]},
                "redis": {"level": "WARNING", "handlers": ["console"]},
                "aiokafka": {"level": "WARNING", "handlers": ["console"]},
                "asyncpg": {"level": "WARNING", "handlers": ["console"]},
            },
            "disable_existing_loggers": False,
        }
    )

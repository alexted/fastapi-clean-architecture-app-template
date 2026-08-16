import logging
import logging.config
import sys
from typing import TYPE_CHECKING

from pythonjsonlogger.json import JsonFormatter

if TYPE_CHECKING:
    from .settings import AppConfig


class OTelJsonFormatter(JsonFormatter):
    """Custom formatter for correct processing of OpenTelemetry data."""

    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)

        trace_id = getattr(record, "otelTraceID", None)
        span_id = getattr(record, "otelSpanID", None)

        if trace_id and trace_id != "0":
            log_record["trace_id"] = trace_id
        if span_id and span_id != "0":
            log_record["span_id"] = span_id

        service_name = getattr(record, "otelServiceName", None)
        if service_name:
            log_record["service"] = service_name


def init_logging(config: AppConfig) -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:trace=%(otelTraceID)s\n%(message)s\n",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "json": {
                    "()": OTelJsonFormatter,
                    "format": "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "json_ensure_ascii": False,
                },
            },
            "handlers": {
                "console": {
                    "level": config.LOG_LEVEL,
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default" if config.ENVIRONMENT == "dev" else "json",
                }
            },
            "loggers": {
                config.APP_NAME: {"level": config.LOG_LEVEL, "handlers": ["console"], "propagate": False},
                "granian": {"level": "INFO", "handlers": ["console"], "propagate": False},
                "granian.access": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "granian.error": {"level": "ERROR", "handlers": ["console"], "propagate": False},
                "fastapi": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "sqlalchemy.engine": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "alembic": {"level": "INFO", "handlers": ["console"], "propagate": False},
                "httpx2": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "redis": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "aiokafka": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "asyncpg": {"level": "WARNING", "handlers": ["console"], "propagate": False},
            },
        }
    )

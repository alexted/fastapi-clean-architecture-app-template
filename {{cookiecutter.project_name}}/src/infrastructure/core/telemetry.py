from __future__ import annotations

from typing import TYPE_CHECKING

from opentelemetry import trace
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPX2ClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

# NOTE! enable only if you plan to send traces somewhere other than Sentry
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

if TYPE_CHECKING:
    from fastapi import FastAPI

    from src.infrastructure.core.settings import AppConfig


def setup_otel(config: AppConfig, app: FastAPI) -> None:
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": config.APP_NAME,
                "service.namespace": "backend",
                "deployment.environment": config.ENVIRONMENT,
            }
        )
    )
    trace.set_tracer_provider(provider)

    # NOTE! enable only if you plan to send traces somewhere other than Sentry
    # otlp_exporter = OTLPSpanExporter(endpoint=config.TELEMETRY_URL)
    # span_processor = BatchSpanProcessor(
    #     otlp_exporter,
    #     max_queue_size=2048,
    #     batch_size=512,
    #     schedule_delay_millis=5000
    # )
    # provider.add_span_processor(span_processor)

    LoggingInstrumentor().instrument(set_logging_format=False)
    FastAPIInstrumentor().instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
    RedisInstrumentor().instrument()
    AIOKafkaInstrumentor().instrument()
    HTTPX2ClientInstrumentor().instrument()

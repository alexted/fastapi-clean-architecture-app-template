from __future__ import annotations

from typing import TYPE_CHECKING

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

# enable only if you plan to send traces somewhere other than Sentry
# import socket
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

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
                # "service.instance.id": socket.gethostname(),
            }
        )
    )
    trace.set_tracer_provider(provider)

    # enable only if you plan to send traces somewhere other than Sentry
    # otlp_exporter = OTLPSpanExporter(endpoint=config.TELEMETRY_URL)
    # span_processor = BatchSpanProcessor(
    #     otlp_exporter,
    #     max_queue_size=2048,
    #     batch_size=512,
    #     schedule_delay_millis=5000
    # )
    # provider.add_span_processor(span_processor)

    FastAPIInstrumentor().instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
    RedisInstrumentor().instrument()
    AIOKafkaInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()

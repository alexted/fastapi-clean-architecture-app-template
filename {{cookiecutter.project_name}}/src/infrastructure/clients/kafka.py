from __future__ import annotations

import json
from typing import TYPE_CHECKING, Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from src.infrastructure.core.settings import AppConfig, get_config

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


_producer_instance: AIOKafkaProducer | None = None


async def init_kafka_producer(config: Annotated[AppConfig, Depends(get_config)]) -> AIOKafkaProducer:
    """Initialize Kafka producer instance."""
    global _producer_instance

    if _producer_instance is None:
        _producer_instance = AIOKafkaProducer(
            bootstrap_servers=config.KAFKA_DSN,
            value_serializer=lambda value: json.dumps(value).encode(),
            compression_type="gzip",
        )
        _producer_instance._closed = None

    return _producer_instance


async def get_kafka_producer(
    producer: Annotated[AIOKafkaProducer, Depends(init_kafka_producer)],
) -> AsyncGenerator[AIOKafkaProducer]:
    """Provides the Kafka producer instance."""
    if producer._closed is None:
        await producer.start()
        producer._closed = False

    yield producer

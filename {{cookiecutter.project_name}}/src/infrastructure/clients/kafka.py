from __future__ import annotations

from functools import lru_cache
import json
from typing import TYPE_CHECKING, Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from src.infrastructure.core.settings import AppConfig, get_config

if TYPE_CHECKING:
    from collections.abc import Iterator


@lru_cache(maxsize=1)
def init_kafka_producer(config: Annotated[AppConfig, Depends(get_config)]) -> AIOKafkaProducer:
    """Initialize Kafka producer instance."""
    producer = AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_DSN.unicode_string(),
        value_serializer=lambda value: json.dumps(value).encode(),
        compression_type="gzip",
    )
    producer._closed = None
    return producer


async def get_kafka_producer(
    producer: Annotated[AIOKafkaProducer, Depends(init_kafka_producer)],
) -> Iterator[AIOKafkaProducer]:
    """Provides Kafka producer instance."""
    if producer._closed is None:
        await producer.start()
        producer._closed = False
    yield producer

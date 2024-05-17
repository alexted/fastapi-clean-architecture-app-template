from collections.abc import Iterator

from aiokafka import AIOKafkaProducer

from src.service.config import config

producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_DSN)


async def get_kafka_producer() -> Iterator[AIOKafkaProducer]:
    await producer.start()
    yield producer

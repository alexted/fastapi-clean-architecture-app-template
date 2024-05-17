from collections.abc import Iterator

from redis.asyncio import Redis, ConnectionPool

from src.service.config import config

pool = ConnectionPool.from_url(config.REDIS_DSN)


async def get_redis_client() -> Iterator[Redis]:
    client = Redis.from_pool(pool)
    yield client

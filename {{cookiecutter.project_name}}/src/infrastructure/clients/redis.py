from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from src.infrastructure.core.settings import AppConfig, get_config

_redis_client: Redis | None = None


async def get_cache_client(config: Annotated[AppConfig, Depends(get_config)]) -> Redis:
    """Provides Redis client."""
    global _redis_client

    if _redis_client is None:
        _redis_client = Redis(
            host=config.CACHE_DSN.host, port=config.CACHE_DSN.port, decode_responses=True, client_name=config.APP_NAME
        )

    return _redis_client

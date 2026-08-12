from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from src.infrastructure.clients.kafka import get_kafka_producer
from src.infrastructure.clients.postgres.engine import get_db_session
from src.infrastructure.clients.redis import get_cache_client

if TYPE_CHECKING:
    from aiokafka import AIOKafkaProducer
    from redis.asyncio import Redis
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

health_routes = APIRouter(tags=["infrastructure"])


@health_routes.get("/health/live", summary="Liveness probe")
async def liveness_probe() -> JSONResponse:
    """
    K8s calls this to check if the process in the pod is stuck.
    If it returns 500 or times out — the pod will be killed and restarted.
    """
    return JSONResponse(status_code=HTTP_200_OK, content="alive")


async def _check_postgres(session: AsyncSession) -> bool:
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.exception(f"Postgres readiness check failed: {e}")
        return False


async def _check_redis(redis_client: Redis) -> bool:
    try:
        return await redis_client.ping()
    except Exception as e:
        logger.exception(f"Redis readiness check failed: {e}")
        return False


async def _check_kafka(producer: AIOKafkaProducer) -> bool:
    try:
        cluster_metadata = await producer.client.fetch_all_metadata()
        return len(cluster_metadata.brokers()) > 0
    except Exception as e:
        logger.exception(f"Kafka readiness check failed: {e}")
        return False


@health_routes.get("/health/ready", summary="Readiness probe")
async def readiness_probe(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    redis_client: Annotated[Redis, Depends(get_cache_client)],
    kafka_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> JSONResponse:
    """
    K8s calls this to check if traffic can be routed to the pod.
    If it returns 503 — traffic will stop being sent, but the pod will not die.
    """
    TIMEOUT_SECONDS = 3.0

    try:
        results = await asyncio.wait_for(
            asyncio.gather(_check_postgres(db_session), _check_redis(redis_client), _check_kafka(kafka_producer)),
            timeout=TIMEOUT_SECONDS,
        )

        postgres_ok, redis_ok, kafka_ok = results

        components = {
            "postgres": "up" if postgres_ok else "down",
            "redis": "up" if redis_ok else "down",
            "kafka": "up" if kafka_ok else "down",
        }

        if not all(results):
            return JSONResponse(
                status_code=HTTP_503_SERVICE_UNAVAILABLE
                # Опционально можно отдавать JSON с упавшими сервисами для дебага
                # content=json.dumps({"status": "error", "components": components})
            )

        return {"status": "ok", "components": components}

    except TimeoutError:
        logger.exception("Readiness probe timed out")
        return JSONResponse(status_code=HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as err:
        logger.exception(f"Unexpected error in readiness probe: {err}")
        return JSONResponse(status_code=HTTP_503_SERVICE_UNAVAILABLE)

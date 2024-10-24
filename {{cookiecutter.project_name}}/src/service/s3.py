from typing import Any, Annotated
from functools import lru_cache
from collections.abc import AsyncIterator

from fastapi import Depends
import aioboto3

from src.service.config import AppConfig, get_config


@lru_cache(maxsize=1)
def get_s3_session(config: Annotated[AppConfig, Depends(get_config)]) -> aioboto3.Session:
    """Provides S3 connection"""
    return aioboto3.Session(
        aws_access_key_id=config.S3_ACCESS_KEY,
        aws_secret_access_key=config.S3_SECRET_KEY,
        region_name=config.AWS_REGION_NAME,
    )


async def get_s3_client(
    s3_session: Annotated[aioboto3.Session, Depends(get_s3_session)], config: Annotated[AppConfig, Depends(get_config)]
) -> AsyncIterator[Any]:
    """Provides S3 client"""
    async with s3_session.client("s3", endpoint_url=config.S3_URL) as s3_client:
        yield s3_client

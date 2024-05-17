import contextlib
import functools

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Query

from src.service.config import config

engine: AsyncEngine = create_async_engine(
    config.POSTGRES_DSN.unicode_string(),
    pool_size=config.POSTGRES_MAX_CONNECTIONS,
    pool_pre_ping=True,
    pool_recycle=60,
)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> Iterator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session

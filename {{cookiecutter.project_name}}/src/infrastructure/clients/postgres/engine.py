from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from src.infrastructure.core.settings import AppConfig

engine: AsyncEngine = None
session_factory: async_sessionmaker[AsyncSession] = None


def init_database(config: AppConfig) -> None:
    global engine, session_factory

    engine = create_async_engine(
        config.POSTGRES_DSN.unicode_string(),
        pool_size=config.POSTGRES_MAX_CONNECTIONS,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=True,
        connect_args={
            "server_settings": {"application_name": f"{config.APP_NAME.lower()}[{config.ENVIRONMENT.lower()}]"}
        },
    )

    session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    session = session_factory()
    try:
        yield session
        # При необходимости можно автоматически коммитить, если не было исключений
        # await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

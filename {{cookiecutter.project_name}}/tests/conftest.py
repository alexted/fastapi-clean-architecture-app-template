import uuid
from typing import BinaryIO
import asyncio
from asyncio import AbstractEventLoop
from collections.abc import Iterator, AsyncIterator, AsyncGenerator

from httpx import AsyncClient, ASGITransport
import pytest
from fastapi import FastAPI
from sqlalchemy import NullPool
from alembic.config import Config as AlembicConfig
from alembic.command import upgrade, downgrade
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from tests.data import mock_data
from src.service.config import get_config
from src.service.application import create_app
from src.service.postgres.engine import get_db_session


TEST_APP_URL = "http://test"

pytest_plugins = ("tests.fixtures.items",)


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest) -> Iterator[AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    """
    # Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
    """
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def migrations() -> None:
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.attributes["configure_logger"] = False

    upgrade(alembic_config, "head")
    yield "on head"
    downgrade(alembic_config, "base")


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    return create_async_engine(get_config().POSTGRES_DSN.unicode_string(), poolclass=NullPool)


@pytest.fixture(autouse=True)
async def db_session(db_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """
    Create a transactional test database session.
    https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    # expose session
    async with async_sessionmaker(db_engine, expire_on_commit=False).begin() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
def app(migrations: None, db_session: AsyncSession) -> FastAPI:
    app_instance = create_app()

    def get_db_session_override() -> Iterator[AsyncSession]:
        try:
            yield db_session
        finally:
            pass

    app_instance.dependency_overrides[get_db_session] = get_db_session_override

    return app_instance


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=TEST_APP_URL,
        headers={"Authorization": f"Bearer {mock_data.employees[0]["id"]}"},
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def seed_data(db_session: AsyncSession) -> None:
    ...
    # db_session.add_all([Project(**_) for _ in mock_data.projects])
    # db_session.add_all([User(**_) for _ in mock_data.users])
    # await db_session.flush()
    # db_session.add_all([Employee(**_) for _ in mock_data.employees])
    # db_session.add_all([UserProjectRole(**_) for _ in mock_data.user_project_roles])
    # db_session.add_all([Department(**_) for _ in mock_data.departments])
    # await db_session.flush()

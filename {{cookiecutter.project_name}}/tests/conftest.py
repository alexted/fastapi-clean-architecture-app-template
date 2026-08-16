from typing import TYPE_CHECKING, Any

from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
import asyncpg
from httpx2 import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.clients.postgres.engine import get_db_session
from src.infrastructure.core.application import create_app
from src.infrastructure.core.settings import AppConfig, get_config
from tests.data import mock_data

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, AsyncIterator, Iterator

TEST_APP_URL = "http://test"

pytest_plugins = ("tests.fixtures.items",)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    # Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def db_engine(worker_id: str) -> AsyncIterator[AsyncEngine]:
    config: AppConfig = get_config()
    db_dsn: str = config.POSTGRES_DSN.unicode_string().replace("+asyncpg", "")
    schema: str = f"test_{worker_id}"

    conn: asyncpg.Connection = await asyncpg.connect(db_dsn)
    try:
        await conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
    finally:
        await conn.close()

    engine: AsyncEngine = create_async_engine(
        config.POSTGRES_DSN.unicode_string(),
        echo=False,
        pool_size=config.POSTGRES_MAX_CONNECTIONS,
        pool_pre_ping=True,
        connect_args={"server_settings": {"application_name": schema, "search_path": schema}},
    )

    yield engine

    await engine.dispose()

    conn: asyncpg.Connection = await asyncpg.connect(db_dsn)
    try:
        await conn.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')
    finally:
        await conn.close()


@pytest.fixture(scope="session", autouse=True)
async def migrations(db_engine: AsyncEngine) -> AsyncGenerator[str, Any]:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.attributes["configure_logger"] = False

    def run_upgrade(connection) -> None:
        alembic_cfg.attributes["connection"] = connection
        upgrade(alembic_cfg, "head")

    async with db_engine.begin() as conn:
        await conn.run_sync(run_upgrade)

    yield "on head" # noqa: PT022


@pytest.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """
    Create a transactional test database session.
    https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    connection = await db_engine.connect()
    transaction = await connection.begin()
    async_session = async_sessionmaker(bind=connection, expire_on_commit=False)
    session = async_session()

    try:
        yield session
    finally:
        await session.rollback()
        await session.close()
        await transaction.rollback()
        await connection.close()


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


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=TEST_APP_URL,
        headers={"Authorization": f"Bearer {mock_data.items[0]['id']}"},
    ) as client:
        yield client

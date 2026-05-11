from __future__ import annotations

import asyncio
from logging.config import fileConfig
import threading
import traceback
from typing import TYPE_CHECKING, Any

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.infrastructure.clients.postgres.models import Base
from src.infrastructure.core.settings import AppConfig, get_config

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

app_config: AppConfig = get_config()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=app_config.POSTGRES_DSN.unicode_string(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable = async_engine_from_config(
        {"sqlalchemy.url": app_config.POSTGRES_DSN.unicode_string()},
        # config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def _run_async_migrations_in_thread() -> None:
    """
    Helper wrapper: executes `asyncio.run(run_async_migrations())` in a separate thread.
    Used strictly as a fallback when an event loop is already running and no connection has been provided.
    """
    exc_holder: dict[str, Any] = {"exc": None, "tb": None}

    def _worker() -> None:
        try:
            asyncio.run(run_async_migrations())
        except Exception as exc:
            exc_holder["exc"] = exc
            exc_holder["tb"] = traceback.format_exc()

    thread = threading.Thread(target=_worker)
    thread.start()
    thread.join()

    if exc_holder["exc"] is not None:
        raise RuntimeError("Async alembic migrations failed in worker thread:\n" + exc_holder["tb"]) from exc_holder[
            "exc"
        ]


def run_migrations_online() -> None:
    """
    Universal migration execution logic for 'online' mode.

    Behavior:
    1) If the caller provides `config.attributes['connection']`, it is used directly:
       - If it is an AsyncConnection (has `run_sync`),
       we invoke `connection.run_sync(do_run_migrations)`.
       - Otherwise, it is treated as a synchronous Connection,
       and `do_run_migrations(connection)` is called.
    2) Otherwise, the standard asynchronous path is initiated via `run_async_migrations()`:
       - If an event loop is already running in the current thread,
       the async path is executed in a separate thread as a fallback.
    """
    cfg_connection = context.config.attributes.get("connection")
    if cfg_connection is not None:
        if hasattr(cfg_connection, "run_sync"):
            cfg_connection.run_sync(do_run_migrations)
        else:
            do_run_migrations(cfg_connection)
        return

    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if running_loop is None or not running_loop.is_running():
        asyncio.run(run_async_migrations())
    else:
        _run_async_migrations_in_thread()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from typing import Any
import asyncio
import threading
import traceback
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.infrastructure.core.settings import AppConfig, get_config
from src.infrastructure.clients.postgres.models import Base

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
    Вспомогательная обёртка: запускает asyncio.run(run_async_migrations()) в отдельном потоке.
    Используется только как фолбэк, если мы оказались в уже запущенном loop и нет переданного connection.
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
    Универсальная логика запуска миграций в 'online' режиме.

    Поведение:
    1) Если caller передал `config.attributes['connection']` — используем его.
       - Если это AsyncConnection (имеет run_sync) — вызываем connection.run_sync(do_run_migrations)
       - Иначе считаем его sync Connection и вызываем do_run_migrations(connection)
    2) Иначе — запускаем стандартный async-путь через run_async_migrations().
       - Если в текущем потоке есть запущенный event loop, то как фолбэк запускаем async-путь в отдельном потоке.
    """
    cfg_connection = context.config.attributes.get("connection")
    if cfg_connection is not None:
        # Определяем асинхронное ли это подключение (duck-typing)
        if hasattr(cfg_connection, "run_sync"):
            # AsyncConnection: run_sync примет do_run_migrations(sync_conn)
            # cfg_connection может быть sqlalchemy.ext.asyncio.Connection
            # в таком случае run_sync — coroutine method? В doc: connection.run_sync(sync_callable)
            cfg_connection.run_sync(do_run_migrations)
        else:
            # Sync Connection — вызываем напрямую
            do_run_migrations(cfg_connection)
        return

    # Нет переданного connection — стандартный путь (создаём свой async engine)
    # Но не вызываем asyncio.run() если loop уже живёт в этом процессе.
    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if running_loop is None or not running_loop.is_running():
        # обычный путь (CLI)
        asyncio.run(run_async_migrations())
    else:
        # фолбэк: запускаем в отдельном потоке, чтобы не ломать существующий loop
        _run_async_migrations_in_thread()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

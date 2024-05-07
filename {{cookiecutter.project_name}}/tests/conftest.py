import pytest

from src.service.application import create_app
{% if cookiecutter.use_postgresql|lower == 'y' %}
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig

from src.data.postgres.engine import session_scope
from src.data.postgres.models import Base, Item
from tests.moks_data import items
{% endif %}


@pytest.fixture
def app():
    app_instance = create_app()
    return app_instance

{% if cookiecutter.use_postgresql|lower == 'y' %}

@pytest.fixture(scope='session')
def db_session():
    config = AlembicConfig('alembic.ini')
    config.attributes['configure_logger'] = False

    upgrade(config, 'head')

    yield 'on head'

    downgrade(config, 'base')


@pytest.fixture(autouse=True)
async def clear_data(db_session):
    yield 'I will clear tables for you'

    reference_value_tables = [f'{name}' for name in ('role',)]

    async with session_scope() as session:
        for name, table in Base.metadata.tables.items():
            if name not in reference_value_tables:
                await session.execute(table.delete())


@pytest.fixture
async def fill_db(event_loop):
    items_list = [Item(**item) for item in items]
    async with session_scope() as session:
        session.add_all(items_list)
        await session.flush()
{% endif -%}
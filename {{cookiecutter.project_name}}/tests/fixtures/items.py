{% if cookiecutter.use_postgresql | lower == 'y' -%}
import uuid
from datetime import datetime
from collections.abc import AsyncGenerator
{% endif -%}

import pytest
{% if cookiecutter.use_postgresql | lower == 'y' -%}
from tests.data import mock_data
{% endif -%}
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def seed_item_type(db_session: AsyncSession) -> None:
    ...


@pytest.fixture
async def seed_item(db_session: AsyncSession) -> None:
    ...

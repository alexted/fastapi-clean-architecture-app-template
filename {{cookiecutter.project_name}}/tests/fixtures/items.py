import uuid
from datetime import datetime
from collections.abc import AsyncGenerator

import pytest
from tests.data import mock_data
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def seed_item_type(db_session: AsyncSession) -> None:
    ...


@pytest.fixture
async def seed_item(item_type: Any, db_session: AsyncSession) -> None:
    ...

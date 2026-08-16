from typing import TYPE_CHECKING

import pytest

from src.infrastructure.clients.postgres.models import Item
from tests.data.mock_data import items

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def seed_items(db_session: AsyncSession) -> None:
    db_session.add_all([Item(**_) for _ in items])
    await db_session.flush()

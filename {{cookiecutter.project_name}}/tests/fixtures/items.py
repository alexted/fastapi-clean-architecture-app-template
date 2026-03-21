from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.data.mock_data import items
from src.infrastructure.clients.postgres.models import Item

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def seed_items(db_session: AsyncSession) -> None:
    db_session.add_all([Item(**_) for _ in items])
    await db_session.flush()

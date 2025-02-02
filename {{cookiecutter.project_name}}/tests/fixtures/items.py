import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.postgres.models import Item
from tests.data.mock_data import items


@pytest.fixture
async def seed_items(db_session: AsyncSession) -> None:
    pass
    db_session.add_all([Item(**_) for _ in items])
    await db_session.flush()

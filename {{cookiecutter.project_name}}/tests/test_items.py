import pytest
from httpx import AsyncClient

from tests.expected_data import created_item
from tests.moks_data import items

pytestmark = pytest.mark.asyncio


async def test_create_item(app):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.post('/v1/items', json={
            "name": "TestName",
            "description": "Test description",
            "price": 100
        })

    assert response.status_code == 200
    assert response.json() == created_item


async def test_get_item(event_loop, fill_db, app):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/v1/items/2')

    assert response.status_code == 200
    assert response.json() == items[1]

import pytest
from httpx import AsyncClient

from tests.data.expected_data import created_item
from tests.data.mock_data import items

pytestmark = pytest.mark.anyio


async def test_create_item(client):
    response = await client.post('/v1/items', json={
        "name": "TestName",
        "description": "Test description",
        "price": 100
    })

    assert response.status_code == 200
    assert response.json() == created_item


async def test_get_item(event_loop, fill_db, client):
    response = await client.get('/v1/items/2')

    assert response.status_code == 200
    assert response.json() == items[1]

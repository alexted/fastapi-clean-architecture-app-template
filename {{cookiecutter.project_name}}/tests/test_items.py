import pytest

from tests.data.expected_data import created_item
from tests.data.mock_data import items

pytestmark = pytest.mark.anyio


async def test_create_item(client):
    response = await client.post('/v1/items', json={
        "name": "Item 1",
        "description": "This is awesome item!",
        "price": 100
    })

    assert response.status_code == 201
    assert response.json() == created_item


async def test_get_item(fill_db, client):
    response = await client.get('/v1/items/102')

    assert response.status_code == 200
    assert response.json() == items[1]

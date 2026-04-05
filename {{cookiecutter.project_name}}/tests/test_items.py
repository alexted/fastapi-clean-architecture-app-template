from __future__ import annotations

import pytest

from tests.data.expected_data import created_item, updated_item
from tests.data.mock_data import items

pytestmark = pytest.mark.anyio


async def test_create_item(client) -> None:
    response = await client.post(
        "/v1/items", json={"name": "Item 4", "description": "This is awesome item!", "price": 400}
    )

    assert response.status_code == 201
    assert response.json() == created_item


async def test_list_items(seed_items, client) -> None:
    response = await client.get("/v1/items")

    assert response.status_code == 200
    assert response.json() == items


async def test_get_item(seed_items, client) -> None:
    response = await client.get("/v1/items/102")

    assert response.status_code == 200
    assert response.json() == items[1]


async def test_update_item(seed_items, client) -> None:
    response = await client.put("/v1/items/102", json={"name": "Item 444", "price": 444})

    assert response.status_code == 200
    assert response.json() == updated_item


async def test_delete_item(seed_items, client) -> None:
    response = await client.delete("/v1/items/102")

    assert response.status_code == 204

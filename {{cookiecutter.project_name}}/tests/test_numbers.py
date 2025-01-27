import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_sum(client):
    response = await client.post('/v1/summarise', json={"x": 4, "y": 6})

    assert response.status_code == 200
    assert response.json() == {"sum": 10}

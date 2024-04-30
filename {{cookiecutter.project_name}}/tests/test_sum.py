import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_sum(app):
    async with AsyncClient(app=app, base_url='http://127.0.0.1:5000') as ac:
        response = await ac.post('/v1/sum', json={"x": 4, "y": 6})

    assert response.status_code == 200
    assert response.json() == {"sum": 10}

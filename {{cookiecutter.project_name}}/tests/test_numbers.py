import pytest

pytestmark = pytest.mark.anyio


async def test_sum(client):
    response = await client.post('/v1/summarise', json={"x": 4, "y": 6})

    assert response.status_code == 200
    assert response.json() == {"sum": 10}

async def test_sub(client):
    response = await client.get('/v1/subtract', json={"x": 9, "y": 4})

    assert response.status_code == 200
    assert response.json() == {"sum": 5}


async def test_multi(client):
    response = await client.put('/v1/multiply', json={"x": 3, "y": 3})

    assert response.status_code == 200
    assert response.json() == {"sum": 9}


async def test_div(client):
    response = await client.delete('/v1/divide', json={"x": 9, "y": 3})

    assert response.status_code == 200
    assert response.json() == {"sum": 3}

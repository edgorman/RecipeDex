import pytest

from backend import __description__
from backend import __version__
from backend import __name__


@pytest.mark.asyncio
async def test_root(client):
    async with client as c:
        response = await c.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": __name__,
        "version": __version__,
        "description": __description__
    }

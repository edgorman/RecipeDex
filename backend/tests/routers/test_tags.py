import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_get_all_recipes(mocker, client, mock_tags):
    mocker.patch("backend.routers.tags.get_tags", side_effect=AsyncMock(return_value=mock_tags))

    async with client as c:
        response = await c.get("/tags/")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_tags,
        "message": "Tag data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_tags_by_key(mocker, client, mock_tags):
    mocker.patch("backend.routers.tags.get_tags", side_effect=AsyncMock(return_value=mock_tags))

    async with client as c:
        response = await c.get("/tags/?name=test")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_tags,
        "message": "Tag data retrieved successfully"
    }

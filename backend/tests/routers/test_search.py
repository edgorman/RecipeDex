import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_get_recipes_by_search(mocker, client, mock_tags, mock_index):
    mocker.patch("backend.routers.search.get_tags", side_effect=AsyncMock(return_value=mock_tags))
    mocker.patch("backend.routers.search.get_recipes", side_effect=AsyncMock(return_value=mock_index))

    async with client as c:
        response = await c.get("/search/?t=test&t=this")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_index,
        "message": "Recipe data retrieved successfully"
    }

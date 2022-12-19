import pytest


@pytest.mark.asyncio
async def test_get_recipes_by_search(client, mock_index):
    async with client as c:
        response = await c.get("/search/?t=test&t=this")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_index,
        "message": "Search data retrieved successfully"
    }

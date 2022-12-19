import pytest


@pytest.mark.asyncio
async def test_get_all_recipes(client, mock_tags):
    async with client as c:
        response = await c.get("/tags/")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_tags,
        "message": "Tag data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_tags_by_key(client, mock_tags):
    async with client as c:
        response = await c.get("/tags/?name=test")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_tags,
        "message": "Tag data retrieved successfully"
    }

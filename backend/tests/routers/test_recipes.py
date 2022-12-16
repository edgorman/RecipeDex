import pytest
from urllib.parse import quote
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_get_all_recipes(mocker, client, mock_index):
    get_recipes = AsyncMock(return_value=mock_index)
    mocker.patch("backend.routers.recipes.get_recipes", side_effect=get_recipes)

    async with client as c:
        response = await c.get("/recipes/")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_index,
        "message": "Recipe data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_recent_recipes(mocker, client, mock_index):
    recent_cache = AsyncMock(return_value=mock_index)
    mocker.patch("backend.routers.recipes.recent_cache", side_effect=recent_cache)

    async with client as c:
        response = await c.get("/recipes/recent")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_index,
        "message": "Recipe data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_recipe_by_url(mocker, client, mock_recipe):
    add_recipe = AsyncMock()
    mocker.patch("backend.routers.recipes.add_recipe", side_effect=add_recipe)
    check_cache = AsyncMock(return_value=None)
    mocker.patch("backend.routers.recipes.check_cache", side_effect=check_cache)

    async with client as c:
        response = await c.get(f"/recipes/{quote(mock_recipe['url'])}")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": {mock_recipe["url"]: mock_recipe},
        "message": "Recipe data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_recipe_by_cache(mocker, client, mock_recipe):
    check_cache = AsyncMock(return_value=mock_recipe)
    mocker.patch("backend.routers.recipes.check_cache", side_effect=check_cache)

    async with client as c:
        response = await c.get(f"/recipes/{quote(mock_recipe['url'])}")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": {mock_recipe["url"]: mock_recipe},
        "message": "Recipe data retrieved successfully"
    }

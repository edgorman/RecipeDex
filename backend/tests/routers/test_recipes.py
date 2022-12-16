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
        url = quote(mock_recipe["url"])
        response = await c.get(f"/recipes/{url}")

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
        url = quote(mock_recipe["url"])
        response = await c.get(f"/recipes/{url}")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": {mock_recipe["url"]: mock_recipe},
        "message": "Recipe data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_recipe_and_scale(mocker, client, mock_recipe):
    check_cache = AsyncMock(return_value=mock_recipe)
    mocker.patch("backend.routers.recipes.check_cache", side_effect=check_cache)

    async with client as c:
        url = quote(mock_recipe["url"])
        serves = mock_recipe["servings"] * 2
        response = await c.get(f"/recipes/{url}?serves={serves}")

    mock_recipe["servings"] = serves
    for i in range(len(mock_recipe["ingredient_list"])):
        mock_recipe["ingredient_list"][i]["quantity"] = str(round(
            float(mock_recipe["ingredient_list"][i]["quantity"]) * 2,
            2
        ))
    
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": {mock_recipe["url"]: mock_recipe},
        "message": "Recipe data retrieved successfully"
    }

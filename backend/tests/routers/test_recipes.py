import pytest
from urllib.parse import quote


@pytest.mark.asyncio
async def test_get_all_recipes(client, mock_index):
    async with client as c:
        response = await c.get("/recipes/")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_index,
        "message": "Recipe data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_recent_recipes(client, mock_index):
    async with client as c:
        response = await c.get("/recipes/recent")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "data": mock_index,
        "message": "Recipe data retrieved successfully"
    }


@pytest.mark.asyncio
async def test_get_recipe_by_url(client, mock_recipe):
    # TODO: Use client that returns None object for check_cache

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
async def test_get_recipe_by_cache(client, mock_recipe):
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
async def test_get_recipe_and_scale(client, mock_recipe):
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

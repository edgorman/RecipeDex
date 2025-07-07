import json
import pytest
from internal.objects.recipe import Recipe, RecipeRole


@pytest.fixture
def mock_recipe_dict():
    return {
        "id": "123",
        "private": False,
        "user_access_mapping": {
            "abc": RecipeRole.UNDEFINED.value,
            "def": RecipeRole.VIEWER.value,
            "ghi": RecipeRole.EDITOR.value,
            "jkl": RecipeRole.OWNER.value
        }
    }


@pytest.fixture
def mock_recipe(mock_recipe_dict):
    return Recipe(
        id=mock_recipe_dict["id"],
        private=mock_recipe_dict["private"],
        user_access_mapping={
            k: RecipeRole(v) for k, v in mock_recipe_dict["user_access_mapping"].items()
        }
    )


def test_to_dict(mock_recipe, mock_recipe_dict):
    assert mock_recipe.to_dict() == mock_recipe_dict


def test_to_json(mock_recipe, mock_recipe_dict):
    json_str = mock_recipe.to_json()
    assert isinstance(json_str, str)
    assert json.loads(json_str) == mock_recipe_dict


def test_from_dict(mock_recipe, mock_recipe_dict):
    recipe = Recipe.from_dict(mock_recipe_dict)
    assert isinstance(recipe, Recipe)
    assert recipe == mock_recipe


def test_from_json(mock_recipe, mock_recipe_dict):
    recipe = Recipe.from_json(json.dumps(mock_recipe_dict))
    assert isinstance(recipe, Recipe)
    assert recipe == mock_recipe

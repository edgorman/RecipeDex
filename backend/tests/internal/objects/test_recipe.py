import pytest
from uuid import uuid4, UUID
from internal.objects.recipe import Recipe, RecipeRole


@pytest.fixture
def mock_recipe_dict():
    return {
        "id": str(uuid4()),
        "private": False,
        "user_access_mapping": {
            str(uuid4()): RecipeRole.UNDEFINED.value,
            str(uuid4()): RecipeRole.VIEWER.value,
            str(uuid4()): RecipeRole.EDITOR.value,
            str(uuid4()): RecipeRole.OWNER.value
        }
    }


@pytest.fixture
def mock_recipe(mock_recipe_dict):
    return Recipe(
        id=UUID(mock_recipe_dict["id"]),
        private=mock_recipe_dict["private"],
        user_access_mapping={
            UUID(k): RecipeRole(v) for k, v in mock_recipe_dict["user_access_mapping"].items()
        }
    )


def test_to_dict(mock_recipe, mock_recipe_dict):
    assert mock_recipe.to_dict() == mock_recipe_dict


def test_from_dict(mock_recipe, mock_recipe_dict):
    recipe = Recipe.from_dict(mock_recipe_dict)
    assert isinstance(recipe, Recipe)
    assert recipe == mock_recipe

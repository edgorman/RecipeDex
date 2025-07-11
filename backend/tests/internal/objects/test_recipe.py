import pytest
from uuid import uuid4, UUID
from internal.objects.recipe import Recipe


@pytest.fixture
def mock_recipe_dict():
    return {
        "id": str(uuid4()),
        "name": "mock_recipe",
        "private": False,
        "deleted": False,
        "user_access_mapping": {
            str(uuid4()): Recipe.Role.UNDEFINED.value,
            str(uuid4()): Recipe.Role.VIEWER.value,
            str(uuid4()): Recipe.Role.EDITOR.value,
            str(uuid4()): Recipe.Role.OWNER.value
        },
        "ingredients": [],
        "instructions": []
    }


@pytest.fixture
def mock_recipe(mock_recipe_dict):
    return Recipe(
        id=UUID(mock_recipe_dict["id"]),
        name=mock_recipe_dict["name"],
        private=mock_recipe_dict["private"],
        user_access_mapping={
            UUID(k): Recipe.Role(v) for k, v in mock_recipe_dict["user_access_mapping"].items()
        },
        ingredients=[
            Recipe.Ingredient(
                name=ingredient["name"],
                unit=ingredient["unit"],
                quantity=ingredient["quantity"]
            )
            for ingredient in mock_recipe_dict["ingredients"]
        ],
        instructions=[
            Recipe.Instruction(
                value=instruction["value"]
            )
            for instruction in mock_recipe_dict["instructions"]
        ]
    )


def test_to_dict(mock_recipe, mock_recipe_dict):
    assert mock_recipe.to_dict() == mock_recipe_dict


def test_from_dict(mock_recipe, mock_recipe_dict):
    recipe = Recipe.from_dict(mock_recipe_dict)
    assert isinstance(recipe, Recipe)
    assert recipe == mock_recipe

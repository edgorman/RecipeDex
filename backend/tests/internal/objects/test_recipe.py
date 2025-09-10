import pytest
from datetime import datetime, timezone
from uuid import uuid4, UUID

from internal.objects.recipe import Recipe


@pytest.fixture
def mock_recipe_dict():
    return {
        "id": str(uuid4()),
        "name": "mock_recipe",
        "private": False,
        "deleted": False,
        "user_session_mapping": {},
        "user_role_mapping": {
            str(uuid4()): Recipe.Role.UNDEFINED.value,
            str(uuid4()): Recipe.Role.VIEWER.value,
            str(uuid4()): Recipe.Role.EDITOR.value,
            str(uuid4()): Recipe.Role.OWNER.value
        },
        "ingredients": [],
        "instructions": [],
        "created_at": datetime.now(tz=timezone.utc).isoformat().replace('+00:00', 'Z'),
        "updated_at": datetime.now(tz=timezone.utc).isoformat().replace('+00:00', 'Z'),
        "deleted_at": datetime.now(tz=timezone.utc).isoformat().replace('+00:00', 'Z'),
    }


@pytest.fixture
def mock_recipe(mock_recipe_dict):
    return Recipe(
        id=UUID(mock_recipe_dict["id"]),
        name=mock_recipe_dict["name"],
        private=mock_recipe_dict["private"],
        user_role_mapping={
            UUID(k): Recipe.Role(v) for k, v in mock_recipe_dict["user_role_mapping"].items()
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
        ],
        created_at=datetime.fromisoformat(mock_recipe_dict["created_at"]),
        updated_at=datetime.fromisoformat(mock_recipe_dict["updated_at"]),
        deleted_at=datetime.fromisoformat(mock_recipe_dict["deleted_at"]),
    )


def test_to_dict(mock_recipe, mock_recipe_dict):
    assert mock_recipe.to_dict() == mock_recipe_dict


def test_from_dict(mock_recipe, mock_recipe_dict):
    recipe = Recipe.from_dict(mock_recipe_dict)
    assert isinstance(recipe, Recipe)
    assert recipe == mock_recipe


def test_owner_id(mock_recipe_dict):
    mock_recipe_clone = mock_recipe_dict.copy()

    mock_owner_id = uuid4()
    mock_recipe_clone["user_role_mapping"] = {str(mock_owner_id): Recipe.Role.OWNER.value}
    mock_recipe = Recipe.from_dict(mock_recipe_clone)

    owner_id = mock_recipe.owner_id
    assert owner_id == mock_owner_id

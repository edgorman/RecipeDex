import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone

from internal.objects.recipe import Recipe


@pytest.fixture
def owner_id() -> UUID:
    """Returns a UUID for the owner."""
    return uuid4()


@pytest.fixture
def recipe(owner_id: UUID) -> Recipe:
    """Returns a basic Recipe object."""
    return Recipe(
        id=uuid4(),
        name="Test Recipe",
        user_role_mapping={owner_id: Recipe.Role.OWNER}
    )


@pytest.mark.parametrize(
    "name, private",
    [
        ("Test Recipe 1", False),
        ("Another Recipe", True),
        ("A very long recipe name to test limits", False),
    ]
)
def test_recipe_creation(owner_id: UUID, name: str, private: bool):
    """
    Test that a Recipe object can be created with different parameters.

    Args:
        owner_id: the ID of the owner.
        name: the name of the recipe.
        private: the privacy status of the recipe.
    """
    recipe_id = uuid4()
    recipe = Recipe(
        id=recipe_id,
        name=name,
        private=private,
        user_role_mapping={owner_id: Recipe.Role.OWNER}
    )
    assert recipe.id == recipe_id
    assert recipe.name == name
    assert recipe.private == private
    assert recipe.user_role_mapping == {owner_id: Recipe.Role.OWNER}
    assert recipe.ingredients == []
    assert recipe.instructions == []
    assert isinstance(recipe.created_at, datetime)
    assert isinstance(recipe.updated_at, datetime)
    assert recipe.deleted_at is None


@pytest.mark.parametrize(
    "deleted_time, is_deleted_expected",
    [
        (None, False),
        (datetime.now(tz=timezone.utc), True),
    ]
)
def test_is_deleted(recipe: Recipe, deleted_time: datetime, is_deleted_expected: bool):
    """
    Test the is_deleted property.

    Args:
        recipe: the recipe to test.
        deleted_time: the time the recipe was deleted.
        is_deleted_expected: the expected value of the is_deleted property.
    """
    recipe.deleted_at = deleted_time
    assert recipe.is_deleted == is_deleted_expected


def test_owner_id(recipe: Recipe, owner_id: UUID):
    """
    Test the owner_id property.

    Args:
        recipe: the recipe to test.
        owner_id: the expected owner ID.
    """
    assert recipe.owner_id == owner_id


def test_owner_id_no_owner():
    """Test that owner_id raises ValueError if no owner is set."""
    recipe = Recipe(id=uuid4(), name="Test Recipe")
    with pytest.raises(ValueError, match="no owner mapping exists in this Recipe"):
        _ = recipe.owner_id


def test_display_id(recipe: Recipe):
    """
    Test the display_id property.

    Args:
        recipe: the recipe to test.
    """
    assert recipe.display_id == str(recipe.id)


def test_display_name(recipe: Recipe):
    """
    Test the display_name property.

    Args:
        recipe: the recipe to test.
    """
    assert recipe.display_name == recipe.name


@pytest.mark.parametrize(
    "name, unit, quantity",
    [
        ("flour", "grams", 500),
        ("sugar", "cups", 1.5),
        ("salt", "teaspoon", 0.5),
    ]
)
def test_ingredient_creation(name: str, unit: str, quantity: float):
    """
    Test that an Ingredient object can be created with different parameters.

    Args:
        name: the name of the ingredient.
        unit: the unit of the ingredient.
        quantity: the quantity of the ingredient.
    """
    ingredient = Recipe.Ingredient(name=name, unit=unit, quantity=quantity)
    assert ingredient.name == name
    assert ingredient.unit == unit
    assert ingredient.quantity == quantity


@pytest.mark.parametrize(
    "value",
    [
        "Mix flour and water.",
        "Bake at 350 degrees for 30 minutes.",
        "Let cool before serving.",
    ]
)
def test_instruction_creation(value: str):
    """
    Test that an Instruction object can be created with different parameters.

    Args:
        value: the value of the instruction.
    """
    instruction = Recipe.Instruction(value=value)
    assert instruction.value == value


@pytest.mark.parametrize(
    "role, value",
    [
        (Recipe.Message.Role.USER, "Hello"),
        (Recipe.Message.Role.MODEL, "Hi there!"),
        (Recipe.Message.Role.UNDEFINED, "Some message"),
    ]
)
def test_message_creation(role: Recipe.Message.Role, value: str):
    """
    Test that a Message object can be created with different parameters.

    Args:
        role: the role of the message sender.
        value: the value of the message.
    """
    message = Recipe.Message(role=role, value=value)
    assert message.role == role
    assert message.value == value

import pytest
from uuid import uuid4
from unittest.mock import Mock

from internal.objects.recipe import Recipe
from internal.objects.user import User
from internal.agent.vertex.tools.recipe import create_get_recipe_tools, create_update_recipe_tools


example_recipe = Recipe(
    id=uuid4(),
    name="example_recipe",
    private=False,
    ingredients=[Recipe.Ingredient(name="flour", unit="grams", quantity=500)],
    instructions=[Recipe.Instruction(value="mix it")]
)
example_user = User(
    id=uuid4(),
    name="example_user",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
        info={}
    )
)


@pytest.fixture
def mock_recipe_storage_handler():
    return Mock()


@pytest.fixture
def mock_tool_context():
    return Mock()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "get_field,expected_value",
    [
        ("name", example_recipe.name),
        ("private", example_recipe.private),
        ("ingredients", [ingredient.model_dump(mode="json") for ingredient in example_recipe.ingredients]),
        ("instructions", [instruction.model_dump(mode="json") for instruction in example_recipe.instructions]),
    ]
)
async def test_get_recipe_field_tool(
    mock_recipe_storage_handler,
    mock_tool_context,
    get_field,
    expected_value
):
    mock_tool_context.state.get.return_value = example_recipe.id
    mock_recipe_storage_handler.get.return_value = example_recipe

    tool = create_get_recipe_tools(mock_recipe_storage_handler)[get_field]
    response = await tool.run_async(args={}, tool_context=mock_tool_context)
    assert response["status"] == "success", response["message"]
    assert response["value"] == expected_value

    mock_recipe_storage_handler.get.assert_called_once_with(example_recipe.id)
    mock_recipe_storage_handler.update.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,new_value,expected_status",
    [
        ("name", "new_name", "success"),
        ("private", True, "success"),
        ("ingredients", [{"name": "name", "unit": "unit", "quantity": float(100)}], "success"),
        ("instructions", [{"value": "value"}], "success"),
    ]
)
async def test_update_recipe_name_tool(
    mock_recipe_storage_handler,
    mock_tool_context,
    update_field,
    new_value,
    expected_status
):
    mock_tool_context.state.get.return_value = example_recipe.id
    mock_recipe_storage_handler.get.return_value = example_recipe
    expected_recipe_dump = example_recipe.model_dump(mode="json")
    expected_recipe_dump[update_field] = new_value

    tool = create_update_recipe_tools(mock_recipe_storage_handler)[update_field]
    response = await tool.run_async(args={"new_value": new_value}, tool_context=mock_tool_context)
    assert response["status"] == expected_status, response["message"]

    mock_recipe_storage_handler.get.assert_called_once_with(example_recipe.id)
    mock_recipe_storage_handler.update.assert_called_once()
    assert mock_recipe_storage_handler.update.call_args.args[0] == example_recipe.id

    recipe_dump = mock_recipe_storage_handler.update.call_args.args[1].model_dump(mode="json")
    assert recipe_dump == expected_recipe_dump

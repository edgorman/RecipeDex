from uuid import UUID
from typing import Any, Dict, List
from pydantic import BaseModel
from google.adk.tools import FunctionTool, ToolContext

from internal.storage.recipe import RecipeStorage
from internal.objects.recipe import Recipe
from internal.objects.session import Session


def create_get_recipe_tools(recipe_storage_handler: RecipeStorage) -> Dict[str, FunctionTool]:
    """
    Creates multiple tools used to get a field of a recipe.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A list of FunctionTool objects for getting recipe fields.
    """

    def _get_recipe_field(id_: UUID, field: str, tool_name: str) -> Dict[str, str]:
        """
        Gets the field of a recipe.

        Args:
            id_: The id of the recipe to get.
            field: The field of the recipe to get.
            tool_name: The name of the tool that called this function.

        Returns:
            A dict describing the outcome of the tool usage.
            see https://google.github.io/adk-docs/tools/function-tools/#return-type
        """
        try:
            recipe = recipe_storage_handler.get(id_)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not load recipe from internal storage: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            value = getattr(recipe, field)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not get recipe field `{field}`: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            if isinstance(value, BaseModel):
                value = value.model_dump(mode="json")
            elif isinstance(value, list):
                value = [v.model_dump(mode="json") if isinstance(v, BaseModel) else v for v in value]
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not format value for recipe `{field}`: `{str(e)}`."
            ).model_dump(mode="json")

        return Session.Message.ToolResponse(
            name=tool_name,
            status=Session.Message.ToolResponse.Status.SUCCESS,
            value=value,
            message=f"Recipe {field} retrieved successfully."
        ).model_dump(mode="json")

    def get_recipe_name_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the name field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(
            tool_context.state.get("recipe_id"),
            "name",
            "get_recipe_name_tool"
        )

    def get_recipe_private_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the private field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(
            tool_context.state.get("recipe_id"),
            "private",
            "get_recipe_private_tool"
        )

    def get_recipe_ingredients_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the ingredients field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(
            tool_context.state.get("recipe_id"),
            "ingredients",
            "get_recipe_ingredients_tool"
        )

    def get_recipe_instructions_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the instructions field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(
            tool_context.state.get("recipe_id"),
            "instructions",
            "get_recipe_instructions_tool"
        )

    return {
        "name": FunctionTool(get_recipe_name_tool),
        "private": FunctionTool(get_recipe_private_tool),
        "ingredients": FunctionTool(get_recipe_ingredients_tool),
        "instructions": FunctionTool(get_recipe_instructions_tool),
    }


def create_update_recipe_tools(recipe_storage_handler: RecipeStorage) -> Dict[str, FunctionTool]:
    """
    Creates multiple tools used to update a field of a recipe.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A list of FunctionTool objects for updating recipe fields.
    """

    def _update_recipe_field(id_: UUID, field: str, new_value: Any, tool_name: str) -> Dict[str, str]:
        """
        Updates the field of a recipe.

        Args:
            id_: The id of the recipe to update.
            field: the field of the recipe to update.
            new_value: The new value for the field.
            tool_name: The name of the tool that called this function.

        Returns:
            A dict describing the outcome of the tool usage.
            see https://google.github.io/adk-docs/tools/function-tools/#return-type
        """
        try:
            recipe = recipe_storage_handler.get(id_)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not load recipe from internal storage: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            setattr(recipe, field, new_value)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not update recipe {field} to `{new_value}`: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            recipe_storage_handler.update(id_, recipe)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not store recipe update: `{str(e)}`."
            ).model_dump(mode="json")

        return Session.Message.ToolResponse(
            name=tool_name,
            status=Session.Message.ToolResponse.Status.SUCCESS,
            message=f"Recipe {field} updated"
        ).model_dump(mode="json")

    def update_recipe_name_tool(new_value: str, tool_context: ToolContext) -> Dict[str, str]:
        """
        Updates the name field of the recipe.

        Args:
            new_value: The new name of the recipe.
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _update_recipe_field(
            tool_context.state.get("recipe_id"),
            "name",
            new_value,
            "update_recipe_name_tool"
        )

    def update_recipe_private_tool(new_value: bool, tool_context: ToolContext) -> Dict[str, str]:
        """
        Updates the private field of the recipe.

        Args:
            new_value: The new private value of the recipe.
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _update_recipe_field(
            tool_context.state.get("recipe_id"),
            "private",
            new_value,
            "update_recipe_private_tool"
        )

    def update_recipe_ingredients_tool(
        new_value: List[Recipe.Ingredient],
        tool_context: ToolContext
    ) -> Dict[str, str]:
        """
        Updates the ingredients field of the recipe.

        Args:
            new_value: The new ingredients value of the recipe.
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        try:
            if not isinstance(new_value, list):
                new_value = [new_value]
            ingredients = [Recipe.Ingredient.model_validate(ingredient) for ingredient in new_value]
        except Exception as e:
            return Session.Message.ToolResponse(
                name="update_recipe_ingredients_tool",
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not parse new value to ingredient: `{str(e)}`."
            ).model_dump(mode="json")

        return _update_recipe_field(
            tool_context.state.get("recipe_id"),
            "ingredients",
            ingredients,
            "update_recipe_ingredients_tool"
        )

    def update_recipe_instructions_tool(
        new_value: List[Recipe.Instruction],
        tool_context: ToolContext
    ) -> Dict[str, str]:
        """
        Updates the instructions field of the recipe.

        Args:
            new_value: The new instructions value of the recipe.
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        try:
            if not isinstance(new_value, list):
                new_value = [new_value]
            instructions = [Recipe.Instruction.model_validate(instruction) for instruction in new_value]
        except Exception as e:
            return Session.Message.ToolResponse(
                name="update_recipe_instructions_tool",
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not parse new value to instruction: `{str(e)}`."
            ).model_dump(mode="json")

        return _update_recipe_field(
            tool_context.state.get("recipe_id"),
            "instructions",
            instructions,
            "update_recipe_instructions_tool"
        )

    return {
        "name": FunctionTool(update_recipe_name_tool),
        "private": FunctionTool(update_recipe_private_tool),
        "ingredients": FunctionTool(update_recipe_ingredients_tool),
        "instructions": FunctionTool(update_recipe_instructions_tool),
    }

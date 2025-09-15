from uuid import UUID
from typing import Any, Dict, List
from pydantic import BaseModel
from google.adk.tools import FunctionTool, ToolContext

from internal.storage.recipe import RecipeStorage
from internal.objects.recipe import Recipe


def create_get_recipe_tools(recipe_storage_handler: RecipeStorage) -> Dict[str, FunctionTool]:
    """
    Creates multiple tools used to get a field of a recipe.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A list of FunctionTool objects for getting recipe fields.
    """

    def _get_recipe_field(id_: UUID, field: str) -> Dict[str, str]:
        """
        Gets the field of a recipe.

        Args:
            id_: The id of the recipe to get.
            field: the field of the recipe to get.

        Returns:
            A dict describing the outcome of the tool usage.
            see https://google.github.io/adk-docs/tools/function-tools/#return-type
        """
        try:
            recipe = recipe_storage_handler.get(id_)
        except Exception as e:
            return {"status": "error", "message": f"Could not load recipe from internal state: `{str(e)}`."}

        try:
            value = getattr(recipe, field)
        except Exception as e:
            return {"status": "error", "message": f"Could not get recipe {field}: `{str(e)}`."}

        try:
            if isinstance(value, BaseModel):
                value = value.model_dump(mode="json")
            elif isinstance(value, list):
                value = [v.model_dump(mode="json") if isinstance(v, BaseModel) else v for v in value]
        except Exception as e:
            return {"status": "error", "message": f"Could not format recipe {field}: `{str(e)}`"}

        return {"status": "success", "value": value, "message": f"Recipe {field} retrieved"}

    def get_recipe_name_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the name field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(tool_context.state.get("recipe_id"), "name")

    def get_recipe_private_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the private field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(tool_context.state.get("recipe_id"), "private")

    def get_recipe_ingredients_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the ingredients field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(tool_context.state.get("recipe_id"), "ingredients")

    def get_recipe_instructions_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the instructions field of the recipe.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_recipe_field(tool_context.state.get("recipe_id"), "instructions")

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

    def _update_recipe_field(id_: UUID, field: str, new_value: Any) -> Dict[str, str]:
        """
        Updates the field of a recipe.

        Args:
            id_: The id of the recipe to update.
            field: the field of the recipe to update.
            new_value: The new value for the field.

        Returns:
            A dict describing the outcome of the tool usage.
            see https://google.github.io/adk-docs/tools/function-tools/#return-type
        """
        try:
            recipe = recipe_storage_handler.get(id_)
        except Exception as e:
            return {"status": "error", "message": f"Could not load recipe from internal state: `{str(e)}`."}

        try:
            setattr(recipe, field, new_value)
        except Exception as e:
            return {"status": "error", "message": f"Could not update recipe {field} to `{new_value}`: `{str(e)}`."}

        try:
            recipe_storage_handler.update(id_, recipe)
        except Exception as e:
            return {"status": "error", "message": f"Could not store recipe update: `{str(e)}`."}

        return {"status": "success", "message": f"Recipe {field} updated"}

    def update_recipe_name_tool(new_value: str, tool_context: ToolContext) -> Dict[str, str]:
        """
        Updates the name field of the recipe.

        Args:
            new_value: The new name of the recipe.
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _update_recipe_field(tool_context.state.get("recipe_id"), "name", new_value)

    def update_recipe_private_tool(new_value: bool, tool_context: ToolContext) -> Dict[str, str]:
        """
        Updates the private field of the recipe.

        Args:
            new_value: The new private value of the recipe.
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _update_recipe_field(tool_context.state.get("recipe_id"), "private", new_value)

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
            return {"status": "error", "message": f"Could not parse new value to ingredient: `{str(e)}`."}

        return _update_recipe_field(tool_context.state.get("recipe_id"), "ingredients", ingredients)

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
            return {"status": "error", "message": f"Could not parse new value to instruction: `{str(e)}`."}

        return _update_recipe_field(tool_context.state.get("recipe_id"), "instructions", instructions)

    # We strictly define what fields an agent is able to update here
    # It is good practice having multiple functions because the agent will use the
    # paramters, type hints and doc strings to infer how each tool should be used
    return {
        "name": FunctionTool(update_recipe_name_tool),
        "private": FunctionTool(update_recipe_private_tool),
        "ingredients": FunctionTool(update_recipe_ingredients_tool),
        "instructions": FunctionTool(update_recipe_instructions_tool),
    }

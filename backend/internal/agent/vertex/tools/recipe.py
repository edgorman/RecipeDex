from uuid import UUID
from google.adk.tools import FunctionTool

from internal.storage.recipe import RecipeStorage


def create_update_recipe_name_tool(recipe_storage_handler: RecipeStorage) -> FunctionTool:
    """
    Creates a tool to update the name field of a recipe.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A FunctionTool object for updating recipe names.
    """

    def update_recipe_name_tool(new_name: str, recipe_id: str) -> str:
        """
        Updates the name field of the recipe.

        Args:
            new_name: The new name of the recipe.
            recipe_id: The recipe id to update.

        Returns:
            A confirmation message.
        """
        try:
            recipe = recipe_storage_handler.get(UUID(recipe_id))
        except Exception as e:
            return f"Could not find recipe: {str(e)}"

        try:
            recipe.name = new_name
        except Exception as e:
            return f"Could not update recipe field: {str(e)}"

        try:
            recipe_storage_handler.update(recipe.id, recipe)
        except Exception as e:
            return f"Could not store updated recipe: {str(e)}"

        return f"Recipe name updated to {new_name}."

    return FunctionTool(update_recipe_name_tool)

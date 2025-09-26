from uuid import UUID
from typing import Any, Dict, List
from pydantic import BaseModel
from google.adk.tools import AgentTool, BaseTool, FunctionTool, ToolContext
from recipe_scrapers import scrape_html
from ingredient_slicer import IngredientSlicer

from internal.agent.vertex._subagents.searcher.agent import SearcherAgent
from internal.storage.recipe import RecipeStorage
from internal.objects.recipe import Recipe
from internal.objects.session import Session


def create_get_recipe_tools(recipe_storage_handler: RecipeStorage) -> List[BaseTool]:
    """
    Creates multiple tools used to get a field of a recipe.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A list of tools for getting recipe fields.
    """

    def _get_recipe_field(id_: UUID, field: str) -> Dict[str, str]:
        """
        Gets the field of a recipe.

        Args:
            id_: The id of the recipe to get.
            field: The field of the recipe to get.

        Returns:
            A dict describing the outcome of the tool usage.
            see https://google.github.io/adk-docs/tools/function-tools/#return-type
        """
        tool_name = f"get_recipe_{field}_tool"

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

    return [
        FunctionTool(get_recipe_name_tool),
        FunctionTool(get_recipe_private_tool),
        FunctionTool(get_recipe_ingredients_tool),
        FunctionTool(get_recipe_instructions_tool),
    ]


def create_update_recipe_tools(recipe_storage_handler: RecipeStorage) -> List[BaseTool]:
    """
    Creates multiple tools used to update a field of a recipe.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A list of tools for updating recipe fields.
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
        tool_name = f"update_recipe_{field}_tool"

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
            return Session.Message.ToolResponse(
                name="update_recipe_ingredients_tool",
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not parse new value to ingredient: `{str(e)}`."
            ).model_dump(mode="json")

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
            return Session.Message.ToolResponse(
                name="update_recipe_instructions_tool",
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not parse new value to instruction: `{str(e)}`."
            ).model_dump(mode="json")

        return _update_recipe_field(tool_context.state.get("recipe_id"), "instructions", instructions)

    return [
        FunctionTool(update_recipe_name_tool),
        FunctionTool(update_recipe_private_tool),
        FunctionTool(update_recipe_ingredients_tool),
        FunctionTool(update_recipe_instructions_tool),
    ]


def create_search_recipe_tools(recipe_storage_handler: RecipeStorage) -> List[BaseTool]:
    """
    Creates multiple tools used to search google for recipe content.

    Args:
        recipe_storage_handler: The storage handler for recipes.

    Returns:
        A list of tools for searching recipes.
    """

    def _parse_ingredient(value: str) -> Recipe.Ingredient:
        """
        Parse an ingredient from a scraped string into an Ingredient instance.

        Args:
            value: The ingredient as a string

        Returns:
            An ingredient from the value
        """
        parsed_ingredient = IngredientSlicer(value)

        # Get the unit from the parsed ingredient
        unit = parsed_ingredient.standardized_unit()
        if not unit:
            unit = parsed_ingredient.unit()

        # Get the quantity and convert to float
        try:
            quantity = float(parsed_ingredient.quantity())
        except Exception:
            quantity = None

        return Recipe.Ingredient(
            name=parsed_ingredient.food(),
            unit=unit,
            quantity=quantity
        )

    def _scrape_recipe(url: str, recipe: Recipe) -> None:
        """
        Scrape a recipe from a url and update an existing recipe instance in place.

        Args:
            url: The url of the recipe
            recipe: The recipe to scrape into
        """
        scraped_recipe = scrape_html(None, url, online=True, supported_only=True)
        ingredients = [_parse_ingredient(ingredient) for ingredient in scraped_recipe.ingredients()]
        instructions = [Recipe.Instruction(value=instruction) for instruction in scraped_recipe.instructions_list()]

        recipe.name = scraped_recipe.title()
        recipe.ingredients = ingredients
        recipe.instructions = instructions

    def scrape_recipe_from_url(url: str, tool_context: ToolContext) -> Dict[str, str]:
        """
        Scrapes a recipe from a URL.

        Args:
            value: the search terms to use
            tool_context: the context of the tool usage

        Returns:
            A dict describing the outcome
        """
        tool_name = "scrape_recipe_from_url"

        try:
            # Get the existing recipe from context
            id_ = tool_context.state.get("recipe_id")
            recipe = recipe_storage_handler.get(id_)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not get recipe: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            # Scrape recipe from url in place
            _scrape_recipe(url, recipe)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not scrape recipe: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            # Update the recipe using scraped content
            recipe_storage_handler.update(id_, recipe)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not store recipe: `{str(e)}`."
            ).model_dump(mode="json")

        return Session.Message.ToolResponse(
            name=tool_name,
            status=Session.Message.ToolResponse.Status.SUCCESS,
            message="Recipe scrape ran successfully."
        ).model_dump(mode="json")

    return [FunctionTool(scrape_recipe_from_url), AgentTool(agent=SearcherAgent())]

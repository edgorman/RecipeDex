from uuid import UUID
from typing import Any, Dict, List
from pydantic import BaseModel
from google.adk.tools import FunctionTool, ToolContext
from recipe_scrapers import scrape_html
from ingredient_slicer import IngredientSlicer

from internal.clients.search import SearchClient
from internal.storage.recipe import RecipeStorage
from internal.objects.recipe import Recipe
from internal.objects.session import Session


def create_get_recipe_tools(recipe_storage_handler: RecipeStorage) -> List[FunctionTool]:
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


def create_update_recipe_tools(recipe_storage_handler: RecipeStorage) -> List[FunctionTool]:
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


def create_search_recipe_tools(
    recipe_storage_handler: RecipeStorage,
    search_client: SearchClient
) -> List[FunctionTool]:
    """
    Creates multiple tools used to search google for recipe content.

    Args:
        recipe_storage_handler: The storage handler for recipes.
        search_client: The search client for performing external searches.

    Returns:
        A list of FunctionTool objects for searching recipes.
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
            # TODO: log and handle these units
            quantity = float(0)
            if parsed_ingredient.quantity() is None:
                quantity = float(1)

        return Recipe.Ingredient(
            name=parsed_ingredient.food(),
            unit=unit,
            quantity=quantity
        )

    def _scrape_recipe(url: str, recipe_id: UUID, user_id: UUID) -> Recipe:
        """
        Scrape a recipe from the url given into a Recipe instance.

        Args:
            url: The url of the recipe
            recipe_id: The id of the recipe for the request
            user_id: The id of the user making the request

        Returns:
            A Recipe from the url
        """
        scraped_recipe = scrape_html(None, url, online=True, supported_only=True)
        ingredients = [_parse_ingredient(ingredient) for ingredient in scraped_recipe.ingredients()]
        instructions = [Recipe.Instruction(value=instruction) for instruction in scraped_recipe.instructions_list()]

        return Recipe(
            id=recipe_id,
            name=scraped_recipe.title(),
            ingredients=ingredients,
            instructions=instructions,
            user_role_mapping={user_id: Recipe.Role.OWNER}
        )

    def search_recipes_from_internet(search_query: str, tool_context: ToolContext) -> Dict[str, str]:
        """
        Searches recipes from internet.

        Args:
            search_query: The search terms to use
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        tool_name = "search_recipes_from_internet"

        recipes = []
        errors = []
        page_index = -1

        # Run while loop until limits are hit
        while len(recipes) < 3 and page_index < 9:
            page_index += 1

            try:
                # Get next page of results from search client
                page_urls = search_client.list(search_query, page_index)
            except Exception as e:
                errors.append(f"could not search `{search_query}` at page index {page_index}: {str(e)}")
                continue

            for url in page_urls:
                try:
                    # Scrape the recipe and append to list
                    recipes.append(
                        _scrape_recipe(url, tool_context.state.get("recipe_id"), tool_context.state.get("user_id"))
                    )
                except Exception as e:
                    errors.append(f"could not scrape recipe from `{url}`: {str(e)}")
                    continue

        # Handle worst case where no recipes were scraped
        if len(recipes) == 0:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not scrape recipe(s) from search: `{errors}`."
            ).model_dump(mode="json")

        # Return a successful tool response with scraped recipes as the value
        # Only return the top 3 recipes that were scraped
        return Session.Message.ToolResponse(
            name=tool_name,
            status=Session.Message.ToolResponse.Status.SUCCESS,
            value=recipes[:3],
            message="Recipe search ran successfully."
        ).model_dump(mode="json")

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
            # Scrape recipe from url
            recipe = _scrape_recipe(url, tool_context.state.get("recipe_id"), tool_context.state.get("user_id"))
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not scrape recipe: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            # Update the recipe using scraped content
            id_ = tool_context.state.get("recipe_id")
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

    return [
        FunctionTool(search_recipes_from_internet),
        FunctionTool(scrape_recipe_from_url)
    ]

from google.adk.agents import Agent

from internal.config.agent import AGENT_COORDINATOR_NAME, AGENT_MODEL_NAME
from internal.storage.recipe import RecipeStorage
from internal.storage.user import UserStorage
from internal.agent.vertex._tools.recipe import (
    create_get_recipe_tools, create_update_recipe_tools, create_search_recipe_tools
)
from internal.agent.vertex._tools.user import create_get_user_tools


class CoordinatorAgent(Agent):
    """The CoordinatorAgent is the root agent for all user interactions."""

    def __init__(
        self,
        recipe_storage_handler: RecipeStorage,
        user_storage_handler: UserStorage,
    ) -> None:
        """
        Initialise the CoordinatorAgent class.

        Args:
            recipe_storage_handler: the storage handler for recipes
            user_storage_handler: the storage handler for users
        """
        tools = create_get_recipe_tools(recipe_storage_handler) + \
            create_update_recipe_tools(recipe_storage_handler) + \
            create_search_recipe_tools(recipe_storage_handler) + \
            create_get_user_tools(user_storage_handler)

        super().__init__(
            name=AGENT_COORDINATOR_NAME,
            model=AGENT_MODEL_NAME,
            description="Help users create new recipes or update existing recipes.",
            instruction="""
Role: Act as a recipe and meal planning assistant. Your primary goal is to help users create new recipes or update
existing recipes according to their inputs.

Instructions: At the beginning, introduce yourself to the user first. Say something like:
"Hey {user.name}, I'm your personal recipe assistant! Ready to get started?".

Tools: You may use tools when directed by the user to get/update/create fields of a recipe. You cannot edit recipes
directly, but can change them indirectly via tools. Use the tool names and descriptions to determine which is most
applicable for the user's instructions. When searching the internet for recipes, use the searcher agent tool which
should include a list of recipe URLs, and then scrape it using the `scrape_recipe_from_url` tool.

You may also use tools to get the current user's information, which may be used in recipes (e.g. use their allergy
information to assist the user in making safe choices in regards to ingredients/preperation).
""",
            tools=tools,
        )

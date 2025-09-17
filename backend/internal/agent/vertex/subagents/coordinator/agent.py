from google.adk.agents import Agent

from internal.config.agent import AGENT_COORDINATOR_NAME, AGENT_MODEL_NAME
from internal.storage.recipe import RecipeStorage
from internal.storage.user import UserStorage
from internal.agent.vertex.tools.recipe import create_get_recipe_tools, create_update_recipe_tools
from internal.agent.vertex.tools.user import create_get_user_tools


class CoordinatorAgent(Agent):
    """The CoordinatorAgent is the root agent for all user interactions."""

    def __init__(self, recipe_storage_handler: RecipeStorage, user_storage_handler: UserStorage) -> None:
        """
        Initialise the CoordinatorAgent class.

        Args:
            recipe_storage_handler: the storage handler for recipes
            user_storage_handler: the storage handler for users
        """
        tools = list(create_get_recipe_tools(recipe_storage_handler).values()) + \
            list(create_update_recipe_tools(recipe_storage_handler).values()) + \
            list(create_get_user_tools(user_storage_handler).values())

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
applicable for the user's instructions.

You may also use tools to get the current user's information, which may be used in recipes (e.g. use their allergy
information to assist the user in making safe choices in regards to ingredients/preperation).
""",
            tools=tools,
        )

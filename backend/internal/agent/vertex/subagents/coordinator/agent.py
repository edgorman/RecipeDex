from google.adk.agents import Agent

from internal.config.agent import AGENT_COORDINATOR_NAME, AGENT_MODEL_NAME
from internal.storage.recipe import RecipeStorage
from internal.agent.vertex.tools.recipe import create_update_recipe_tools


class CoordinatorAgent(Agent):
    def __init__(self, recipe_storage_handler: RecipeStorage):
        tools = create_update_recipe_tools(recipe_storage_handler).values()

        super().__init__(
            name=AGENT_COORDINATOR_NAME,
            model=AGENT_MODEL_NAME,
            description="help users create new recipes or update existing recipes.",
            instruction="""
Role: Act as a recipe and meal planning assistant. Your primary goal is to help users create new recipes or update
existing recipes according to their inputs.

Instructions: At the beginning, introduce yourself to the user first. Say something like:
"Hey {user.name}, I'm your personal recipe assistant! Ready to get started?".

Actions: You cannot edit recipes directly, but you can change them indirectly via tools. These tools should only be
used if prompted by the user to create or update a field of the recipe. You do not need the recipe id to call a tool.

The tools you have available are:
 - `update_recipe_name_tool`
""",
            output_key=f"{AGENT_COORDINATOR_NAME}_output",
            tools=tools,
        )

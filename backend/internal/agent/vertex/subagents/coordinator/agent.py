from google.adk.agents import Agent

from internal.config.agent import AGENT_COORDINATOR_NAME, AGENT_MODEL_NAME
from internal.storage.recipe import RecipeStorage
from internal.agent.vertex.tools.recipe import create_update_recipe_name_tool


class CoordinatorAgent(Agent):
    def __init__(self, recipe_storage_handler: RecipeStorage):
        tools = [create_update_recipe_name_tool(recipe_storage_handler)]

        super().__init__(
            name=AGENT_COORDINATOR_NAME,
            model=AGENT_MODEL_NAME,
            description="help users create new recipes or update existing recipes.",
            instruction="""
Role: Act as a recipe and meal planning assistant. Your primary goal is to help users create new recipes or update 
existing recipes according to their inputs.

Instructions: At the beginning, introduce yourself to the user first. Say something like: 
"Hey {user_name}, I'm your personal recipe assistant! Ready to get started?".

Actions: You cannot edit recipes directly, but you can change them indirectly via tools. These tools should only be
used if prompted by the user to create or update a field of the recipe. The `recipe_id` parameter should always be 
`{recipe_id}`. The tools you have available are:
 - `update_recipe_name_tool`
""",
            output_key=f"{AGENT_COORDINATOR_NAME}_output",
            tools=tools,
        )


# Initialise root_agent variable, to be used in adk web development
from google.cloud.firestore import Client as FirestoreClient

from internal.config.storage import STORAGE_PROJECT_ID, STORAGE_DATABASE_NAME, STORAGE_COLLECTION_RECIPE_NAME
from internal.storage.firestore.recipe import FirestoreRecipeStorage

firestore_client = FirestoreClient(STORAGE_PROJECT_ID, database=STORAGE_DATABASE_NAME)
recipe_storage_handler = FirestoreRecipeStorage(
    client=firestore_client, collection_path=(STORAGE_COLLECTION_RECIPE_NAME,)
)

root_agent = CoordinatorAgent(recipe_storage_handler)

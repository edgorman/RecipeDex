import click
from google.adk.runners import Runner as AgentRunner
# from google.cloud.firestore import Client as FirestoreClient  # noqa: F401

from internal.config.service import (  # noqa: F401
    HOST as SERVICE_HOST, PORT as SERVICE_PORT, NAME as SERVICE_NAME
)
from internal.config.gcp import PROJECT_ID as GCP_PROJECT_ID  # noqa: F401
from internal.agents.vertex.recipe import VertexRecipeAgent
from internal.agents.vertex.subagents.coordinator.agent import root_agent as base_agent
from internal.storage.firestore.chat import FirestoreChatStorage
from internal.storage.firestore.user import FirestoreUserStorage
from internal.storage.firestore.recipe import FirestoreRecipeStorage
from internal.service.fastapi.api import FastapiAPIService


@click.Group
def service():
    ...


@service.command
def run():
    firestore_client = None  # FirestoreClient(GCP_PROJECT_ID)
    agent_runner_handler = AgentRunner(
        app_name=SERVICE_NAME, agent=base_agent, artifact_service=None, session_service=None, memory_service=None
    )

    chat_storage_handler = FirestoreChatStorage(client=firestore_client)
    recipe_agent_handler = VertexRecipeAgent(agent_runner=agent_runner_handler, chat_handler=chat_storage_handler)
    recipe_storage_handler = FirestoreRecipeStorage(client=firestore_client)
    user_storage_handler = FirestoreUserStorage(client=firestore_client)

    service = FastapiAPIService(
        host=SERVICE_HOST,
        port=SERVICE_PORT,
        recipe_agent_handler=recipe_agent_handler,
        recipe_storage_handler=recipe_storage_handler,
        user_storage_handler=user_storage_handler,
    )

    service.run()


if __name__ == '__main__':
    service()

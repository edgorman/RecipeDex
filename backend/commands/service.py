import click
from google.adk.runners import Runner as AgentRunner
from google.cloud.firestore import Client as FirestoreClient
from google.adk.artifacts.gcs_artifact_service import GcsArtifactService
from google.adk.memory.vertex_ai_rag_memory_service import VertexAiRagMemoryService
from google.adk.sessions.vertex_ai_session_service import VertexAiSessionService

from internal.config.agent import AGENT_ARTIFACT_BUCKET, AGENT_MEMORY_ID, AGENT_PROJECT_ID, AGENT_PROJECT_REGION
from internal.config.service import SERVICE_NAME, SERVICE_VERSION, SERVICE_HOST, SERVICE_PORT
from internal.config.storage import (
    STORAGE_PROJECT_ID, STORAGE_RECIPE_NAME, STORAGE_RECIPE_VERSION, STORAGE_USER_NAME, STORAGE_USER_VERSION
)
from internal.agent.vertex.recipe import VertexRecipeAgent
from internal.agent.vertex.subagents.coordinator.agent import root_agent as base_agent
from internal.storage.firestore.user import FirestoreUserStorage
from internal.storage.firestore.recipe import FirestoreRecipeStorage
from internal.service.fastapi.api import FastapiAPIService


@click.Group
def service():
    ...


@service.command
def run():
    # Initialise storage client and handlers
    firestore_client = FirestoreClient(STORAGE_PROJECT_ID)
    recipe_storage_handler = FirestoreRecipeStorage(
        client=firestore_client, collection_path=(STORAGE_RECIPE_NAME, STORAGE_RECIPE_VERSION)
    )
    user_storage_handler = FirestoreUserStorage(
        client=firestore_client, collection_path=(STORAGE_USER_NAME, STORAGE_USER_VERSION)
    )

    # Initialise agent services and handlers
    agent_artifact_service = GcsArtifactService(bucket_name=AGENT_ARTIFACT_BUCKET)
    agent_memory_service = VertexAiRagMemoryService(
        rag_corpus=f"projects/{AGENT_PROJECT_ID}/locations/{AGENT_PROJECT_REGION}/ragCorpora/{AGENT_MEMORY_ID}"
    )
    agent_sessions_service = VertexAiSessionService(project=AGENT_PROJECT_ID, location=AGENT_PROJECT_REGION)
    agent_runner_service = AgentRunner(
        app_name=SERVICE_NAME,
        agent=base_agent,
        artifact_service=agent_artifact_service,
        memory_service=agent_memory_service,
        session_service=agent_sessions_service
    )
    recipe_agent_handler = VertexRecipeAgent(agent_runner_service=agent_runner_service)

    # Initialise main service and run
    service = FastapiAPIService(
        name=SERVICE_NAME,
        version=SERVICE_VERSION,
        host=SERVICE_HOST,
        port=SERVICE_PORT,
        recipe_agent_handler=recipe_agent_handler,
        recipe_storage_handler=recipe_storage_handler,
        user_storage_handler=user_storage_handler,
    )
    service.run()


if __name__ == '__main__':
    service()

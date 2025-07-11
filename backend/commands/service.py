import click
from google.adk.runners import Runner as AgentRunner
from google.cloud.firestore import Client as FirestoreClient
from google.adk.artifacts.gcs_artifact_service import GcsArtifactService
from google.adk.memory.vertex_ai_rag_memory_service import VertexAiRagMemoryService
from google.adk.sessions.vertex_ai_session_service import VertexAiSessionService

from internal.config.service import (
    HOST as SERVICE_HOST, PORT as SERVICE_PORT, NAME as SERVICE_NAME
)
from internal.config.gcp import (
    PROJECT_ID as GCP_PROJECT_ID, PROJECT_REGION as GCP_PROJECT_REGION, ARTIFACT_GCS_BUCKET, MEMORY_RAG_CORPUS_PATH
)
from internal.agents.vertex.recipe import VertexRecipeAgent
from internal.agents.vertex.subagents.coordinator.agent import root_agent as base_agent
from internal.storage.firestore.user import FirestoreUserStorage
from internal.storage.firestore.recipe import FirestoreRecipeStorage
from internal.service.fastapi.api import FastapiAPIService


@click.Group
def service():
    ...


@service.command
def run():
    # Initialise storage client and handlers
    firestore_client = FirestoreClient(GCP_PROJECT_ID)
    recipe_storage_handler = FirestoreRecipeStorage(client=firestore_client, collection_path=("recipe", "0_0_0_0"))
    user_storage_handler = FirestoreUserStorage(client=firestore_client, collection_path=("user", "0_0_0_0"))

    # Initialise agent services and handlers
    agent_artifact_service = GcsArtifactService(bucket_name=ARTIFACT_GCS_BUCKET)
    agent_memory_service = VertexAiRagMemoryService(rag_corpus=MEMORY_RAG_CORPUS_PATH)
    agent_sessions_service = VertexAiSessionService(project=GCP_PROJECT_ID, location=GCP_PROJECT_REGION)
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
        host=SERVICE_HOST,
        port=SERVICE_PORT,
        recipe_agent_handler=recipe_agent_handler,
        recipe_storage_handler=recipe_storage_handler,
        user_storage_handler=user_storage_handler,
    )
    service.run()


if __name__ == '__main__':
    service()

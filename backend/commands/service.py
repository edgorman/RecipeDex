import click
from google.adk.runners import Runner as AgentRunner
from google.cloud.firestore import Client as FirestoreClient

from internal.config.agent import AGENT_APP_NAME
from internal.config.auth import AUTH_USER_FIREBASE_AUDIENCE
from internal.config.service import (
    SERVICE_NAME,
    SERVICE_VERSION,
    SERVICE_HOST,
    SERVICE_PORT,
    SERVICE_ALLOWED_ORIGIN
)
from internal.config.storage import (
    STORAGE_PROJECT_ID,
    STORAGE_DATABASE_NAME,
    STORAGE_COLLECTION_RECIPE_NAME,
    STORAGE_COLLECTION_USER_NAME,
    STORAGE_COLLECTION_SESSION_NAME
)
from internal.auth.firebase.user import FirebaseUserAuthenticate
from internal.auth.mac.user import MACUserAuthorize
from internal.agent.vertex.recipe import VertexRecipeAgent
from internal.agent.vertex.subagents.coordinator.agent import CoordinatorAgent
from internal.auth.rbac.recipe import RBACRecipeAuthorize
from internal.storage.firestore.user import FirestoreUserStorage
from internal.storage.firestore.recipe import FirestoreRecipeStorage
from internal.storage.firestore.session import FirestoreSessionStorage
from internal.service.fastapi.api import FastapiAPIService


@click.Group
def service():
    ...


@service.command
def run():
    # Initialise storage client and handlers
    firestore_client = FirestoreClient(STORAGE_PROJECT_ID, database=STORAGE_DATABASE_NAME)
    recipe_storage_handler = FirestoreRecipeStorage(
        client=firestore_client, collection_path=(STORAGE_COLLECTION_RECIPE_NAME,)
    )
    user_storage_handler = FirestoreUserStorage(
        client=firestore_client, collection_path=(STORAGE_COLLECTION_USER_NAME,)
    )

    # Initialise auth handlers
    user_authenticate_handler = FirebaseUserAuthenticate(AUTH_USER_FIREBASE_AUDIENCE)
    user_authorize_handler = MACUserAuthorize()

    # Initialise agent services and handlers
    agent_sessions_service = FirestoreSessionStorage(
        firestore_client, collection_path=(STORAGE_COLLECTION_SESSION_NAME,)
    )
    coordinator_agent = CoordinatorAgent(recipe_storage_handler)
    agent_runner_service = AgentRunner(
        app_name=AGENT_APP_NAME,
        agent=coordinator_agent,
        artifact_service=None,
        memory_service=None,
        session_service=agent_sessions_service
    )
    recipe_agent_handler = VertexRecipeAgent(
        agent_runner_service=agent_runner_service,
        recipe_storage_handler=recipe_storage_handler
    )

    # Initialise main service and run
    service = FastapiAPIService(
        name=SERVICE_NAME,
        version=SERVICE_VERSION,
        host=SERVICE_HOST,
        port=SERVICE_PORT,
        allowed_origins=[SERVICE_ALLOWED_ORIGIN],
        recipe_agent_handler=recipe_agent_handler,
        recipe_storage_handler=recipe_storage_handler,
        recipe_authorize_handler=RBACRecipeAuthorize,
        user_storage_handler=user_storage_handler,
        user_authenticate_handler=user_authenticate_handler,
        user_authorize_handler=user_authorize_handler
    )
    service.run()


if __name__ == '__main__':
    service()

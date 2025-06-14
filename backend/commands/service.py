import click
# from google.cloud.firestore import Client as FirestoreClient  # noqa: F401

from internal.config.service import (  # noqa: F401
    HOST as SERVICE_HOST, PORT as SERVICE_PORT
)
from internal.config.gcp import PROJECT_ID as GCP_PROJECT_ID  # noqa: F401
from internal.storage.firestore.user import FirestoreUserStorage
from internal.storage.firestore.recipe import FirestoreRecipeStorage
from internal.service.fastapi.api import FastapiAPIService


@click.Group
def service():
    ...


@service.command
def run():
    # Initialise adapters
    firestore_client = None  # FirestoreClient(GCP_PROJECT_ID)

    # Initialise handlers
    user_storage_handler = FirestoreUserStorage(client=firestore_client)
    recipe_storage_handler = FirestoreRecipeStorage(client=firestore_client)

    # Initialise service
    service = FastapiAPIService(
        host=SERVICE_HOST,
        port=SERVICE_PORT,
        user_storage_handler=user_storage_handler,
        recipe_storage_handler=recipe_storage_handler,
    )

    # Run service
    service.run()


if __name__ == '__main__':
    service()

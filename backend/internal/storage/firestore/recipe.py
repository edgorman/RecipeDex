from typing import Optional
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage


class FirestoreRecipeStorage(RecipeStorage):

    def __init__(self, client: FirestoreClient):
        self.__client = client

    def get(self, id_: str) -> Optional[Recipe]:
        return None

    def create(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...

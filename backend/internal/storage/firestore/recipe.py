from typing import Optional
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.recipe import Recipe, RecipeRole
from internal.storage.recipe import RecipeStorage


class FirestoreRecipeStorage(RecipeStorage):

    def __init__(self, client: FirestoreClient):
        self.__client = client

    def get(self, id_: str) -> Optional[Recipe]:
        return Recipe(
            id_,
            True,
            {
                "owner": RecipeRole.OWNER,
                "editor": RecipeRole.EDITOR,
                "viewer": RecipeRole.VIEWER,
                "undefined": RecipeRole.UNDEFINED
            }
        )

    def create(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...

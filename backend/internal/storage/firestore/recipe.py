from typing import Optional, Tuple
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage


class FirestoreRecipeStorage(RecipeStorage):

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str] = ("recipe")):
        self.__collection = client.collection(collection_path)

    def get(self, id_: str) -> Optional[Recipe]:
        try:
            result = self.__collection.document(id_)
            document = result.get()
        except Exception as e:
            raise Exception(f"Could not get recipe: `{str(e)}`.")

        if document.exists:
            return Recipe.from_dict(document.to_dict())
        return None

    def create(self, recipe: Recipe) -> None:
        try:
            self.__collection.add(
                document_data=recipe.to_dict(),
                document_id=recipe.id,
            )
        except Exception as e:
            raise Exception(f"Could not create recipe: `{str(e)}`.")

    def update(self, id_: str, **kwargs) -> None:
        raise NotImplementedError()

    def delete(self, id_: str) -> None:
        raise NotImplementedError()

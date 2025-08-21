from typing import Optional, Tuple, List
from uuid import UUID
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage


class FirestoreRecipeStorage(RecipeStorage):

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str]):
        self.__collection = client.collection(*collection_path)
        self.__list_min_offset = 0
        self.__list_min_limit = 1
        self.__list_max_limit = 100

    def get(self, id_: UUID) -> Optional[Recipe]:
        try:
            result = self.__collection.document(str(id_))
            document = result.get()
        except Exception as e:
            raise Exception(f"Could not get recipe: `{str(e)}`.")

        if document.exists:
            return Recipe.from_dict(document.to_dict())
        return None

    def list(self, page: int = 0, page_size: int = 25) -> List[Recipe]:
        try:
            result = self.__collection \
                .where("deleted", "==", False) \
                .order_by("name") \
                .offset(max(self.__list_min_offset, page * page_size)) \
                .limit(min(max(self.__list_min_limit, page_size), self.__list_max_limit)) \
                .get()
            documents = result[:page_size]

            return [
                Recipe.from_dict(document.to_dict())
                for document in documents if document.exists
            ]
        except Exception as e:
            raise Exception(f"Could not list recipes: `{str(e)}`.")

    def create(self, recipe: Recipe) -> None:
        try:
            self.__collection.add(
                document_data=recipe.to_dict(),
                document_id=recipe.display_id,
            )
        except Exception as e:
            raise Exception(f"Could not create recipe: `{str(e)}`.")

    def update(self, id_: UUID, **kwargs) -> None:
        if len(kwargs) == 0:
            raise ValueError("Could not update recipe: `no fields to update`.")

        forbidden_keys = list(filter(lambda key: key in Recipe.forbidden_keys_to_update(), kwargs.keys()))
        if len(forbidden_keys) > 0:
            raise ValueError(f"Could not update recipe: `forbidden field(s) in args: {forbidden_keys}`.")

        processed_kwargs = {}
        for key, item in kwargs.items():
            if not isinstance(item, dict):
                processed_kwargs[key] = item
                continue

            processed_kwargs = {
                f"{key}.{inner_key}": inner_item
                for inner_key, inner_item in item.items()
            }

        try:
            # TODO: need to validate that kwargs only contains keys in class
            #       and the values are the expected type
            self.__collection.document(str(id_)).update(processed_kwargs)
        except Exception as e:
            raise Exception(f"Could not update recipe: `{str(e)}`.")

    def delete(self, id_: UUID) -> None:
        try:
            self.__collection.document(str(id_)).update({"deleted": True})
        except Exception as e:
            raise Exception(f"Could not delete recipe: `{str(e)}`.")

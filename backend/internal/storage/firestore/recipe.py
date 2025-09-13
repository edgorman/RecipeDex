from typing import Optional, Tuple, List
from uuid import UUID
from datetime import datetime, timezone
from google.cloud.firestore import FieldFilter, Client as FirestoreClient

from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage


class FirestoreRecipeStorage(RecipeStorage):
    """The FirestoreRecipeStorage is an implementation of the RecipeStorage that uses Firestore."""

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str]):
        """
        Initialise the FirestoreRecipeStorage.

        Args:
            client: the Firestore client.
            collection_path: the path to the collection.
        """
        self.__collection = client.collection(*collection_path)
        self.__list_min_offset = 0
        self.__list_min_limit = 1
        self.__list_max_limit = 100

    def get(self, id_: UUID) -> Optional[Recipe]:
        """
        Get a recipe by its ID.

        Args:
            id_: the ID of the recipe to get.

        Returns:
            the recipe if it exists, otherwise None.
        """
        try:
            # Get the document from Firestore.
            result = self.__collection.document(str(id_))
            document = result.get()
        except Exception as e:
            raise Exception(f"Could not get recipe: `{str(e)}`.")

        if document.exists:
            return Recipe.model_validate(document.to_dict())
        return None

    def list(self, page: int = 0, page_size: int = 25) -> List[Recipe]:
        """
        List recipes with pagination.

        Args:
            page: the page number to return.
            page_size: the number of items to return per page.

        Returns:
            a list of recipes.
        """
        try:
            # Query Firestore for the recipes.
            results = self.__collection \
                .where(filter=FieldFilter("deleted_at", "==", None)) \
                .order_by("name") \
                .offset(max(self.__list_min_offset, page * page_size)) \
                .limit(min(max(self.__list_min_limit, page_size), self.__list_max_limit)) \
                .get()
            documents = results[:page_size]

            # Return the recipes as a list of Recipe objects.
            return [
                Recipe.model_validate(document.to_dict())
                for document in documents if document.exists
            ]
        except Exception as e:
            raise Exception(f"Could not list recipes: `{str(e)}`.")

    def create(self, recipe: Recipe) -> None:
        """
        Create a new recipe.

        Args:
            recipe: the recipe to create.
        """
        try:
            # Add the recipe to Firestore.
            self.__collection.add(
                document_data=recipe.model_dump(mode="json"),
                document_id=recipe.display_id,
            )
        except Exception as e:
            raise Exception(f"Could not create recipe: `{str(e)}`.")

    def update(self, id_: UUID, recipe: Recipe) -> None:
        """
        Update an existing recipe.

        Args:
            id_: the ID of the recipe to update.
            recipe: the recipe to update.
        """
        try:
            # Update the recipe in Firestore.
            recipe.updated_at = datetime.now(tz=timezone.utc)
            self.__collection.document(str(id_)).set(recipe.model_dump(mode="json"))
        except Exception as e:
            raise Exception(f"Could not update recipe: `{str(e)}`.")

    def delete(self, id_: UUID) -> None:
        """
        Delete a recipe.

        Args:
            id_: the ID of the recipe to delete.
        """
        try:
            # Soft delete the recipe in Firestore.
            self.__collection.document(str(id_)).update({"deleted_at": datetime.now(tz=timezone.utc)})
        except Exception as e:
            raise Exception(f"Could not delete recipe: `{str(e)}`.")

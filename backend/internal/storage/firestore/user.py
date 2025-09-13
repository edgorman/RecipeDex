from typing import Any, Optional, Tuple
from uuid import UUID
from datetime import datetime, timezone
from google.cloud.firestore import FieldFilter, Client as FirestoreClient

from internal.objects.user import User
from internal.storage.user import UserStorage


class FirestoreUserStorage(UserStorage):
    """The FirestoreUserStorage is an implementation of the UserStorage that uses Firestore."""

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str]):
        """
        Initialise the FirestoreUserStorage.

        Args:
            client: the Firestore client.
            collection_path: the path to the collection.
        """
        self.__collection = client.collection(*collection_path)

    def get(self, id_: UUID) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            id_: the ID of the user to get.

        Returns:
            the user if they exist, otherwise None.
        """
        try:
            # Get the document from Firestore.
            document = self.__collection.document(str(id_)).get()
        except Exception as e:
            raise Exception(f"Could not get user: `{str(e)}`.")

        if document.exists:
            return User.model_validate(document.to_dict())
        return None

    def get_by_provider_id(self, id_: Any, type_: User.ProviderType) -> Optional[User]:
        """
        Get a user by their provider ID.

        Args:
            id_: the provider ID of the user to get.
            type_: the provider type of the user to get.

        Returns:
            the user if they exist, otherwise None.
        """
        query = (
            self.__collection
            .where(filter=FieldFilter("deleted_at", "==", None))
            .where(filter=FieldFilter("provider.type", "==", type_.value))
            .where(filter=FieldFilter("provider.id", "==", id_))
        )

        try:
            # Query Firestore for the user.
            documents = query.get()
        except Exception as e:
            raise Exception(f"Could not get user by auth provider: `{str(e)}`.")

        if len(documents) == 0:
            return None
        elif len(documents) > 1:
            raise Exception("Could not get user by auth provider: `more than one user returned`.")

        document = documents[0]
        if document.exists:
            return User.model_validate(document.to_dict())
        return None

    def create(self, user: User) -> None:
        """
        Create a new user.

        Args:
            user: the user to create.
        """
        try:
            # Add the user to Firestore.
            self.__collection.add(user.model_dump(mode="json"), user.display_id)
        except Exception as e:
            raise Exception(f"Could not create user: `{str(e)}`.")

    def update(self, id_: UUID, user: User) -> None:
        """
        Update an existing user.

        Args:
            id_: the ID of the user to update.
            user: the user to update.
        """
        try:
            # Update the user in Firestore.
            user.updated_at = datetime.now(tz=timezone.utc)
            self.__collection.document(str(id_)).set(user.model_dump(mode="json"))
        except Exception as e:
            raise Exception(f"Could not update user: `{str(e)}`.")

    def delete(self, id_: UUID) -> None:
        """
        Delete a user.

        Args:
            id_: the ID of the user to delete.
        """
        try:
            # Soft delete the user in Firestore.
            self.__collection.document(str(id_)).update({"deleted_at": datetime.now(tz=timezone.utc)})
        except Exception as e:
            raise Exception(f"Could not delete user: `{str(e)}`.")

from typing import Any, Optional, Tuple
from uuid import UUID
from google.cloud.firestore import Client as FirestoreClient

from internal.config.auth import AuthProvider
from internal.objects.user import User
from internal.storage.user import UserStorage


class FirestoreUserStorage(UserStorage):

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str] = ("user")):
        self.__collection = client.collection(collection_path)

    def get(self, id_: UUID) -> Optional[User]:
        try:
            document = self.__collection.document(str(id_)).get()
        except Exception as e:
            raise Exception(f"Could not get user: `{str(e)}`.")

        if document.exists:
            return User.from_dict(document.to_dict())
        return None

    def get_by_auth_provider(
        self, provider: AuthProvider, provider_info_path: Tuple[str], provider_info_value: Any
    ) -> Optional[User]:
        provider_info_path = ("provider_info") + provider_info_path

        query = (
            self.__collection
            .where("provider", "==", provider.value)
            .where(".".join(provider_info_path), "==", provider_info_value)
        )

        try:
            documents = query.get()
        except Exception as e:
            raise Exception(f"Could not get user by auth provider: `{str(e)}`.")

        if len(documents) == 0:
            return None
        elif len(documents) > 1:
            raise Exception("Could not get user by auth provider: `more than one user returned`.")

        document = documents[0]
        if document.exists:
            return User.from_dict(document.to_dict())
        return None

    def create(self, user: User) -> None:
        try:
            self.__collection.add(
                document_data=user.to_dict(),
                document_id=str(user.id),
            )
        except Exception as e:
            raise Exception(f"Could not create user: `{str(e)}`.")

    def update(self, id_: UUID, **kwargs) -> None:
        if 'id' in kwargs:
            kwargs.pop('id')

        try:
            document = self.__collection.document(str(id_))
            document.update(kwargs)
        except Exception as e:
            raise Exception(f"Could not update user: `{str(e)}`.")

    def delete(self, id_: UUID) -> None:
        try:
            self.__collection.document(str(id_)).delete()
        except Exception as e:
            raise Exception(f"Could not delete user: `{str(e)}`.")

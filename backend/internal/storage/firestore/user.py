from typing import Optional, Tuple
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.user import User
from internal.storage.user import UserStorage


class FirestoreUserStorage(UserStorage):

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str] = ("user")):
        self.__collection = client.collection(collection_path)

    def get(self, id_: str) -> Optional[User]:
        try:
            document = self.__collection.document(id_).get()
        except Exception as e:
            raise Exception(f"Could not get user: `{str(e)}`.")

        if document.exists:
            return User.from_dict(document.to_dict())
        return None

    def create(self, user: User) -> None:
        try:
            self.__collection.add(
                document_data=user.to_dict(),
                document_id=user.id,
            )
        except Exception as e:
            raise Exception(f"Could not create user: `{str(e)}`.")

    def update(self, id_: str, **kwargs) -> None:
        if 'id' in kwargs:
            kwargs.pop('id')

        try:
            document = self.__collection.document(id_)
            document.update(kwargs)
        except Exception as e:
            raise Exception(f"Could not update user: `{str(e)}`.")

    def delete(self, id_: str) -> None:
        try:
            self.__collection.document(id_).delete()
        except Exception as e:
            raise Exception(f"Could not delete user: `{str(e)}`.")

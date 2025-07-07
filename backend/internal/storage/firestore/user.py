from typing import Optional
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.user import User
from internal.storage.user import UserStorage


__COLLCTION_PATH = ("user")


class FirestoreUserStorage(UserStorage):

    def __init__(self, client: FirestoreClient):
        self.__collection = client.collection(__COLLCTION_PATH)

    def get(self, id_: str) -> Optional[User]:
        try:
            result = self.__collection.document(id_)
            document = result.get()
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

    def update(self) -> None:
        raise NotImplementedError()

    def delete(self) -> None:
        raise NotImplementedError()

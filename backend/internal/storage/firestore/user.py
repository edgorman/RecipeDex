from typing import Optional
from google.cloud.firestore import Client as FirestoreClient

from internal.objects.user import User, AuthProvider
from internal.storage.user import UserStorage


class FirestoreUserStorage(UserStorage):

    def __init__(self, client: FirestoreClient):
        self.__client = client

    def get(self, id_: str) -> Optional[User]:
        return User(id_, "name", AuthProvider.FIREBASE, {})

    def create(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...

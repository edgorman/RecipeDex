from google.cloud.firestore import Client as FirestoreClient

from internal.storage.user import UserStorage


class FirestoreUserStorage(UserStorage):

    def __init__(self, client: FirestoreClient):
        self.__client = client

    def get(self):
        ...

    def create(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...

from typing import List, Tuple
from google.cloud.firestore import Client as FirestoreClient

from internal.config.chat import ChatAuthor
from internal.storage.chat import ChatStorage


class FirestoreChatStorage(ChatStorage):

    def __init__(self, client: FirestoreClient):
        self.__client = client

    def get(self) -> List[Tuple[ChatAuthor, str]]:
        ...

    def create(self, author: ChatAuthor, message: str) -> None:
        ...

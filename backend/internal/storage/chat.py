from abc import ABC, abstractmethod
from typing import List, Tuple

from internal.config.chat import ChatAuthor


class ChatStorage(ABC):

    @abstractmethod
    def get(self) -> List[Tuple[ChatAuthor, str]]:
        ...

    @abstractmethod
    def create(self, author: ChatAuthor, message: str) -> None:
        ...

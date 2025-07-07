from typing import Optional
from abc import ABC, abstractmethod

from internal.objects.user import User


class UserStorage(ABC):

    @abstractmethod
    def get(self, id_: str) -> Optional[User]:
        ...

    @abstractmethod
    def create(self):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def delete(self):
        ...

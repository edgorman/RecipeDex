from typing import Optional
from abc import ABC, abstractmethod

from internal.objects.user import User


class UserStorage(ABC):

    @abstractmethod
    def get(self, id_: str) -> Optional[User]:
        ...

    @abstractmethod
    def create(self, user: User) -> None:
        ...

    @abstractmethod
    def update(self, user: User, **kwargs) -> None:
        ...

    @abstractmethod
    def delete(self, id_: str) -> None:
        ...

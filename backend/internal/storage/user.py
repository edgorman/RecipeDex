from abc import ABC, abstractmethod
from uuid import UUID
from typing import Any, Optional

from internal.objects.user import User


class UserStorage(ABC):
    """The UserStorage maintains user information in storage"""

    @abstractmethod
    def get(self, id_: UUID) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_provider_id(self, id_: Any, type_: User.ProviderType) -> Optional[User]:
        ...

    @abstractmethod
    def create(self, user: User) -> None:
        ...

    @abstractmethod
    def update(self, id_: UUID, user: User) -> None:
        ...

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        ...

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

from internal.objects.user import User
from internal.config.auth import AuthProvider


class UserStorage(ABC):

    @abstractmethod
    def get(self, id_: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_auth_provider(self, provider: AuthProvider, provider_info: Dict[str, Any]) -> Optional[User]:
        ...

    @abstractmethod
    def create(self, user: User) -> None:
        ...

    @abstractmethod
    def update(self, id_: str, **kwargs) -> None:
        ...

    @abstractmethod
    def delete(self, id_: str) -> None:
        ...

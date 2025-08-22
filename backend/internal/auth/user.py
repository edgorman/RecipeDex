from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from internal.objects.user import User


class UserAuthorize(ABC):
    """The UserAuthorize authorizes User interactions with a User resource."""

    @classmethod
    def authorize(cls, user: User, action: User.Action, action_user: User) -> bool:
        ...


class UserAuthenticate(ABC):
    """The UserAuthenticate authenticates Users via a provider and token."""

    @abstractmethod
    def authenticate(self, provider: User.ProviderType, token: Any) -> Tuple[str, str, Dict[str, Any]]:
        ...

from abc import ABC
from typing import Any

from internal.objects.user import User


class UserAuthorize(ABC):
    """The UserAuthorize authorizes User interactions with a User resource."""

    @classmethod
    def authorize(self, user: User, action: Any, action_user: User) -> bool:
        ...

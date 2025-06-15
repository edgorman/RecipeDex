from abc import ABC, abstractmethod
from uuid import UUID

from internal.objects.user import User


class RecipeAgent(ABC):

    @abstractmethod
    async def message(self, user: User, session_id: UUID, message: str) -> None:
        ...

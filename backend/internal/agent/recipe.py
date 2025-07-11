from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from internal.objects.user import User


class RecipeAgent(ABC):
    """The RecipeAgent coordinates messages between the user and LLM"""

    @abstractmethod
    async def message(self, user: User, session_id: UUID, message: str) -> List[str]:
        ...

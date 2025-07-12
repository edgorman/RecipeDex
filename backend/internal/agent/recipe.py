from abc import ABC, abstractmethod
from typing import AsyncGenerator

from internal.objects.user import User
from internal.objects.recipe import Recipe


class RecipeAgent(ABC):
    """The RecipeAgent coordinates messages between the user and LLM"""

    @abstractmethod
    def message(self, user: User, recipe: Recipe, message: str) -> AsyncGenerator[str]:
        ...

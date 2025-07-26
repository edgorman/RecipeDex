from abc import ABC, abstractmethod
from typing import AsyncGenerator

from internal.objects.recipe import Recipe


class RecipeAgent(ABC):
    """The RecipeAgent coordinates messages between the user and LLM"""

    @abstractmethod
    def get_messages(self, recipe: Recipe) -> AsyncGenerator[Recipe.Message]:
        ...

    @abstractmethod
    def create_message(self, recipe: Recipe, message: Recipe.Message) -> AsyncGenerator[Recipe.Message]:
        ...

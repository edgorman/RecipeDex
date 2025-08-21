from abc import ABC, abstractmethod
from typing import AsyncGenerator

from internal.objects.recipe import Recipe
from internal.objects.user import User


class RecipeAgent(ABC):
    """The RecipeAgent coordinates messages between the user and generative AI"""

    @abstractmethod
    def get_messages(self, recipe: Recipe, user: User) -> AsyncGenerator[Recipe.Message]:
        ...

    @abstractmethod
    def create_message(self, recipe: Recipe, user: User, message: Recipe.Message) -> AsyncGenerator[Recipe.Message]:
        ...

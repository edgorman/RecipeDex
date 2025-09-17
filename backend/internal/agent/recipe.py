from abc import ABC, abstractmethod
from typing import AsyncGenerator

from internal.objects.recipe import Recipe
from internal.objects.user import User
from internal.objects.session import Session


class RecipeAgent(ABC):
    """The RecipeAgent coordinates messages between the user and generative AI"""

    @abstractmethod
    def get_messages(self, recipe: Recipe, user: User) -> AsyncGenerator[Session.Message]:
        ...

    @abstractmethod
    def create_message(self, recipe: Recipe, user: User, message: Session.Message) -> AsyncGenerator[Session.Message]:
        ...

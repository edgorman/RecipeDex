from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from internal.objects.recipe import Recipe


class RecipeStorage(ABC):
    """The RecipeStorage maintains recipe information in storage"""

    @abstractmethod
    def get(self, id_: UUID) -> Optional[Recipe]:
        ...

    @abstractmethod
    def create(self, recipe: Recipe) -> None:
        ...

    @abstractmethod
    def update(self, id_: UUID, **kwargs) -> None:
        ...

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        ...

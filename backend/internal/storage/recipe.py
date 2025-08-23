from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from internal.objects.recipe import Recipe


class RecipeStorage(ABC):
    """The RecipeStorage maintains recipe information in storage"""

    @abstractmethod
    def get(self, id_: UUID) -> Optional[Recipe]:
        ...

    @abstractmethod
    def list(self, page: int = 0, page_size: int = 25) -> List[Recipe]:
        ...

    @abstractmethod
    def create(self, recipe: Recipe) -> None:
        ...

    @abstractmethod
    def update(self, id_: UUID, recipe: Recipe) -> None:
        ...

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        ...

from abc import ABC, abstractmethod
from typing import Optional

from internal.objects.recipe import Recipe


class RecipeStorage(ABC):

    @abstractmethod
    def get(self, id_: str) -> Optional[Recipe]:
        ...

    @abstractmethod
    def create(self):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def delete(self):
        ...

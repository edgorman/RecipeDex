from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from internal.objects.recipe import Recipe


class RecipeStorage(ABC):
    """The RecipeStorage maintains recipe information in storage"""

    @abstractmethod
    def get(self, id_: UUID) -> Optional[Recipe]:
        """
        Get a recipe by its ID.

        Args:
            id_: the ID of the recipe to get.

        Returns:
            the recipe if it exists, otherwise None.
        """
        ...

    @abstractmethod
    def list(self, page: int = 0, page_size: int = 25) -> List[Recipe]:
        """
        List recipes with pagination.

        Args:
            page: the page number to return.
            page_size: the number of items to return per page.

        Returns:
            a list of recipes.
        """
        ...

    @abstractmethod
    def create(self, recipe: Recipe) -> None:
        """
        Create a new recipe.

        Args:
            recipe: the recipe to create.
        """
        ...

    @abstractmethod
    def update(self, id_: UUID, recipe: Recipe) -> None:
        """
        Update an existing recipe.

        Args:
            id_: the ID of the recipe to update.
            recipe: the recipe to update.
        """
        ...

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        """
        Delete a recipe.

        Args:
            id_: the ID of the recipe to delete.
        """
        ...

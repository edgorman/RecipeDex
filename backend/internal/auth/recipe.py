from abc import ABC

from internal.objects.recipe import Recipe
from internal.objects.user import User


class RecipeAuthorize(ABC):
    """The RecipeAuthorize authorizes User interactions with a Recipe resource."""

    @classmethod
    def authorize(self, recipe: Recipe, action: Recipe.Action, action_user: User) -> bool:
        ...

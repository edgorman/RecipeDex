from abc import ABC
from enum import Enum

from internal.objects.recipe import Recipe
from internal.objects.user import User


class Role(Enum):
    """
    Enumeration of user roles for recipe access control.
    """
    UNDEFINED = "undefined"
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"


class Action(Enum):
    """
    Enumeration of actions that can be performed on a Recipe.
    """
    GET = "get"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    METADATA = "metadata"
    MESSAGE = "message"


class RecipeAuthorize(ABC):
    """The RecipeAuthorize authorizes User interactions with a Recipe resource."""

    @classmethod
    def authorize(self, recipe: Recipe, action: Action, action_user: User) -> bool:
        ...

import json
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass, asdict


class RecipeAction(Enum):
    GET = "get"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class RecipeRole(Enum):
    UNDEFINED = "undefined"
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"


ROLE_ACTION_MAPPING = {
    RecipeRole.UNDEFINED: {},
    RecipeRole.VIEWER: {RecipeAction.GET},
    RecipeRole.EDITOR: {RecipeAction.GET, RecipeAction.UPDATE},
    RecipeRole.OWNER: {RecipeAction.GET, RecipeAction.CREATE, RecipeAction.UPDATE, RecipeAction.DELETE},
}


@dataclass
class Recipe:
    """Class for storing recipe information"""
    id: str
    private: bool
    user_access_mapping: Dict[str, RecipeRole]

    def authorize(self, user_id: Optional[str], action: RecipeAction) -> bool:
        """Authorize a user trying to access this recipe resource"""
        role = self.user_access_mapping.get(user_id, RecipeRole.UNDEFINED)

        if self.private and role is RecipeRole.UNDEFINED:
            return False

        if role is RecipeRole.UNDEFINED:
            role = RecipeRole.VIEWER

        return action in ROLE_ACTION_MAPPING[role]

    def to_dict(self) -> dict:
        def default(obj):
            if isinstance(obj, RecipeRole):
                return obj.value
            if isinstance(obj, dict):
                return {k: default(v) for k, v in obj.items()}
            if hasattr(obj, "__dict__"):
                return default(obj.__dict__)
            if hasattr(obj, "to_json"):
                return json.loads(obj.to_json())
            if hasattr(obj, "name"):
                return obj.name
            if hasattr(obj, "value"):
                return obj.value
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data: dict) -> "Recipe":
        return Recipe(
            id=data["id"],
            private=data["private"],
            user_access_mapping={k: RecipeRole(v) for k, v in data["user_access_mapping"].items()}
        )

    @staticmethod
    def from_json(data: str) -> "Recipe":
        return Recipe.from_dict(json.loads(data))

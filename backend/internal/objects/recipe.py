from enum import Enum
from uuid import UUID
from typing import Dict, Optional
from dataclasses import dataclass, asdict


class RecipeAction(Enum):
    GET = "get"
    GET_METADATA = "get_metadata"
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
    RecipeRole.EDITOR: {RecipeAction.GET, RecipeAction.GET_METADATA, RecipeAction.UPDATE},
    RecipeRole.OWNER: {
        RecipeAction.GET, RecipeAction.GET_METADATA, RecipeAction.CREATE, RecipeAction.UPDATE, RecipeAction.DELETE
    },
}


@dataclass
class Recipe:
    """Class for storing recipe information"""
    id: UUID
    name: str
    private: bool
    user_access_mapping: Dict[UUID, RecipeRole]

    @property
    def display_id(self) -> str:
        return str(self.id)

    @property
    def display_name(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        def default(obj):
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, RecipeRole):
                return obj.value
            if isinstance(obj, dict):
                return {default(k): default(v) for k, v in obj.items()}
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    @staticmethod
    def from_dict(data: dict) -> "Recipe":
        return Recipe(
            id=UUID(data["id"]),
            name=data["name"],
            private=data["private"],
            user_access_mapping={UUID(k): RecipeRole(v) for k, v in data["user_access_mapping"].items()}
        )

    def authorize(self, user_id: Optional[UUID], action: RecipeAction) -> bool:
        """Authorize a user trying to access this recipe resource"""
        role = self.user_access_mapping.get(user_id, RecipeRole.UNDEFINED)

        if self.private and role is RecipeRole.UNDEFINED:
            return False

        if role is RecipeRole.UNDEFINED:
            role = RecipeRole.VIEWER

        return action in ROLE_ACTION_MAPPING[role]

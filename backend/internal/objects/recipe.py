from enum import Enum
from uuid import UUID
from typing import Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Recipe:
    """Class for storing recipe information"""
    id: UUID
    name: str
    private: bool
    user_access_mapping: Dict[UUID, "Role"]

    class Action(Enum):
        GET = "get"
        GET_METADATA = "get_metadata"
        CREATE = "create"
        UPDATE = "update"
        DELETE = "delete"

    class Role(Enum):
        UNDEFINED = "undefined"
        VIEWER = "viewer"
        EDITOR = "editor"
        OWNER = "owner"

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
            if isinstance(obj, Recipe.Role):
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
            user_access_mapping={UUID(k): Recipe.Role(v) for k, v in data["user_access_mapping"].items()}
        )

    def authorize(self, user_id: Optional[UUID], action: "Action") -> bool:
        """Authorize a user trying to access this recipe resource"""
        role = self.user_access_mapping.get(user_id, Recipe.Role.UNDEFINED)

        if self.private and role is Recipe.Role.UNDEFINED:
            return False

        if role is Recipe.Role.UNDEFINED:
            role = Recipe.Role.VIEWER

        return action in ROLE_ACTION_MAPPING[role]


ROLE_ACTION_MAPPING = {
    Recipe.Role.UNDEFINED: {},
    Recipe.Role.VIEWER: {Recipe.Action.GET},
    Recipe.Role.EDITOR: {Recipe.Action.GET, Recipe.Action.GET_METADATA, Recipe.Action.UPDATE},
    Recipe.Role.OWNER: {
        Recipe.Action.GET, Recipe.Action.GET_METADATA, Recipe.Action.CREATE, Recipe.Action.UPDATE, Recipe.Action.DELETE
    },
}

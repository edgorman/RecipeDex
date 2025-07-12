from enum import Enum
from uuid import UUID
from collections.abc import Iterable
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class Recipe:
    """Object that stores recipe information"""
    id: UUID
    name: str
    session_id: Optional[UUID] = None
    deleted: bool = False
    private: bool = False
    user_access_mapping: Dict[UUID, "Role"] = field(default_factory=dict)

    ingredients: List["Ingredient"] = field(default_factory=list)
    instructions: List["Instruction"] = field(default_factory=list)

    class Action(Enum):
        """Actions that can be performed on a Recipe"""
        GET = "get"
        METADATA = "metadata"
        CREATE = "create"
        UPDATE = "update"
        DELETE = "delete"
        MESSAGE = "message"

    class Role(Enum):
        """The role a user can have with regards to a Recipe"""
        UNDEFINED = "undefined"
        VIEWER = "viewer"
        EDITOR = "editor"
        OWNER = "owner"

    @dataclass
    class Ingredient:
        """Object that stores a single ingredient for a Recipe"""
        name: str
        unit: str
        quantity: float

    @dataclass
    class Instruction:
        """Object that stores a single instruction for a Recipe"""
        value: str

    @dataclass
    class Session:
        class Role(Enum):
            """The role an entity can have within a session"""
            UNDEFINED = "undefined"
            MODEL = "model"
            USER = "user"

    @property
    def is_deleted(self) -> bool:
        return self.deleted

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
            if isinstance(obj, Recipe.Action):
                return obj.value
            if isinstance(obj, Recipe.Ingredient):
                return asdict(obj)
            if isinstance(obj, Recipe.Instruction):
                return asdict(obj)
            if isinstance(obj, dict):
                return {default(k): default(v) for k, v in obj.items()}
            if isinstance(obj, Iterable) and not isinstance(obj, str) and len(obj) > 1:
                return [default(v) for v in obj]
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    @staticmethod
    def from_dict(data: dict) -> "Recipe":
        return Recipe(
            id=UUID(data["id"]),
            name=data["name"],
            deleted=data["deleted"] if "deleted" in data else False,
            private=data["private"] if "private" in data else False,
            user_access_mapping={
                UUID(k): Recipe.Role(v) for k, v in data["user_access_mapping"].items()
            },
            ingredients=[
                Recipe.Ingredient(name=i["name"], unit=i["unit"], quantity=i["quantity"])
                for i in data["ingredients"]
            ],
            instructions=[
                Recipe.Instruction(value=i["value"])
                for i in data["instructions"]
            ]
        )

    def authorize(self, user_id: Optional[UUID], action: "Action") -> bool:
        """Authorize a user trying to access this Recipe resource with action"""
        role = self.user_access_mapping.get(user_id, Recipe.Role.UNDEFINED)

        if self.private and role is Recipe.Role.UNDEFINED:
            return False

        if role is Recipe.Role.UNDEFINED:
            role = Recipe.Role.VIEWER

        return action in ROLE_ACTION_MAPPING[role]


ROLE_ACTION_MAPPING = {
    Recipe.Role.UNDEFINED: {},
    Recipe.Role.VIEWER: {
        Recipe.Action.GET
    },
    Recipe.Role.EDITOR: {
        Recipe.Action.GET,
        Recipe.Action.METADATA,
        Recipe.Action.UPDATE,
        Recipe.Action.MESSAGE
    },
    Recipe.Role.OWNER: {
        Recipe.Action.GET,
        Recipe.Action.METADATA,
        Recipe.Action.CREATE,
        Recipe.Action.UPDATE,
        Recipe.Action.DELETE,
        Recipe.Action.MESSAGE
    }
}

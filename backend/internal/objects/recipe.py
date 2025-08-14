from enum import Enum
from uuid import UUID
from collections.abc import Iterable
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field, is_dataclass
from pydantic import TypeAdapter


@dataclass
class Recipe:
    """Object that stores recipe information"""
    id: UUID
    name: str
    session_id: Optional[str] = None
    deleted: bool = False
    private: bool = False
    user_role_mapping: Dict[UUID, "Role"] = field(default_factory=dict)

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
    class Message():
        """The message between a user and model in a session"""
        author_id: str
        author_role: "Role"
        value: str

        class Role(Enum):
            """The role an entity can have within a message"""
            UNDEFINED = "undefined"
            MODEL = "model"
            USER = "user"

    @property
    def is_deleted(self) -> bool:
        return self.deleted

    @property
    def owner_id(self) -> UUID:
        owner_mapping = next(
            filter(
                lambda i: i[1] == Recipe.Role.OWNER,
                self.user_role_mapping.items()
            ),
            None
        )

        if owner_mapping is None:
            raise ValueError("No owner mapping exists in this Recipe")
        return owner_mapping[0]

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
            if isinstance(obj, Enum):
                return obj.value
            if is_dataclass(obj):
                return default(asdict(obj))
            if isinstance(obj, dict):
                return {default(k): default(v) for k, v in obj.items()}
            if isinstance(obj, Iterable) and not isinstance(obj, str) and len(obj) > 1:
                return [default(v) for v in obj]
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    @staticmethod
    def from_dict(data: dict) -> "Recipe":
        return TypeAdapter(Recipe).validate_python(data)

    @classmethod
    def forbidden_keys_to_update(cls) -> List[str]:
        return ["id"]

    def authorize(self, user_id: Optional[UUID], action: "Action") -> bool:
        """Authorize a user trying to access this Recipe resource with action"""
        role = self.user_role_mapping.get(user_id, Recipe.Role.UNDEFINED)

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

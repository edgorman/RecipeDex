from enum import Enum
from uuid import UUID
from collections.abc import Iterable
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field, is_dataclass
from pydantic import TypeAdapter


@dataclass
class Recipe:
    """Object that stores Recipe information"""
    id: UUID
    name: str
    deleted: bool = False
    private: bool = False
    user_session_mapping: Dict[UUID, str] = field(default_factory=dict)
    user_role_mapping: Dict[UUID, "Role"] = field(default_factory=dict)

    ingredients: List["Ingredient"] = field(default_factory=list)
    instructions: List["Instruction"] = field(default_factory=list)

    class Action(Enum):
        GET = "get"
        GET_METADATA = "get_metadata"
        GET_MESSAGES = "get_messages"
        CREATE = "create"
        UPDATE = "update"
        DELETE = "delete"
        MESSAGE = "message"

    class Role(Enum):
        UNDEFINED = "undefined"
        VIEWER = "viewer"
        EDITOR = "editor"
        OWNER = "owner"

    @dataclass
    class Ingredient:
        name: str
        unit: str
        quantity: float

    @dataclass
    class Instruction:
        value: str

    @dataclass
    class Message:
        role: "Role"
        value: str

        class Role(Enum):
            UNDEFINED = "undefined"
            MODEL = "model"
            USER = "user"

    @property
    def is_deleted(self) -> bool:
        return self.deleted

    @property
    def owner_id(self) -> UUID:
        owner_mapping: Optional[Tuple[UUID, Recipe.Role]] = next(
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

    def to_dict(self) -> Dict[str, Any]:
        def default(obj: Any) -> Any:
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
    def from_dict(data: Dict[str, Any]) -> "Recipe":
        return TypeAdapter(Recipe).validate_python(data)

    @classmethod
    def forbidden_keys_to_update(cls) -> List[str]:
        return ["id"]

    @property
    def generative_ai_actions(self) -> List["Action"]:
        return [Recipe.Action.GET_MESSAGES, Recipe.Action.MESSAGE]

from enum import Enum
from uuid import UUID
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    """Object that stores Recipe information"""
    id: UUID
    name: str
    deleted: bool = False
    private: bool = False
    user_session_mapping: Dict[UUID, str] = Field(default_factory=dict)
    user_role_mapping: Dict[UUID, "Role"] = Field(default_factory=dict)

    ingredients: List["Ingredient"] = Field(default_factory=list)
    instructions: List["Instruction"] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    deleted_at: Optional[datetime] = None

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

    class Ingredient(BaseModel):
        name: str
        unit: str
        quantity: float

    class Instruction(BaseModel):
        value: str

    class Message(BaseModel):
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
        """Convert the Recipe to a dictionary with proper serialization"""
        return self.model_dump(mode='json')

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Recipe":
        """Create a Recipe instance from a dictionary"""
        return Recipe.model_validate(data)

    @staticmethod
    def generative_ai_actions() -> List["Action"]:
        return [Recipe.Action.GET_MESSAGES, Recipe.Action.MESSAGE]

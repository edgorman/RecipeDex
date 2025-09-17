from enum import Enum
from uuid import UUID
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    """Object that stores Recipe information"""
    id: UUID
    name: str
    private: bool = False
    ingredients: List["Ingredient"] = Field(default_factory=list)
    instructions: List["Instruction"] = Field(default_factory=list)
    user_session_mapping: Dict[UUID, str] = Field(default_factory=dict)
    user_role_mapping: Dict[UUID, "Role"] = Field(default_factory=dict)
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

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

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
            raise ValueError("no owner mapping exists in this Recipe")
        return owner_mapping[0]

    @property
    def display_id(self) -> str:
        return str(self.id)

    @property
    def display_name(self) -> str:
        return self.name

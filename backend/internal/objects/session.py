from enum import Enum
from uuid import UUID
from typing import Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


class Session:
    """Collection of models used in session objects"""
    model_config = ConfigDict(extra="forbid")

    class State(BaseModel):
        """Object that will be stored in the state of a session object"""
        recipe_id: UUID
        user_id: UUID

    class Message(BaseModel):
        """Object that represents an interaction between user and agent"""
        role: "Role"
        value: Optional[str] = None
        tool: Optional["ToolResponse"] = None
        created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

        class Role(Enum):
            UNDEFINED = "undefined"
            MODEL = "model"
            USER = "user"
            SYSTEM = "system"

        class ToolResponse(BaseModel):
            """Object that describes the status of a tool used in a session"""
            name: str
            status: "Status"
            value: Optional[Any] = None
            message: Optional[str] = None

            class Status(Enum):
                UNDEFINED = "undefined"
                PENDING = "pending"
                SUCCESS = "success"
                ERROR = "error"

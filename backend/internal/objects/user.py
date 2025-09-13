from enum import Enum
from uuid import UUID
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from starlette.authentication import BaseUser


class User(BaseModel, BaseUser):
    """Object that stores User information"""
    id: UUID
    name: str
    role: "Role"
    provider: "Provider"
    deleted: bool = False

    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    deleted_at: Optional[datetime] = None

    class Action(Enum):
        GET = "get"
        GET_BY_PROVIDER = "get_by_provider"
        CREATE = "create"
        UPDATE = "update"
        DELETE = "delete"

    class Role(Enum):
        UNDEFINED = "undefined"
        ADMIN = "admin"

    class ProviderType(Enum):
        UNDEFINED = "undefined"
        FIREBASE = "firebase"

    class Provider(BaseModel):
        id: Any
        type: "User.ProviderType"
        info: Dict[str, Any]

    @property
    def is_deleted(self) -> bool:
        return self.deleted

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_id(self) -> str:
        return str(self.id)

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def provider_id(self) -> str:
        return self.provider.id

    @property
    def can_call_generative_ai(self) -> bool:
        # for now, only admins are authorized
        # in the future, this will depend on whether the user is paying
        return self.role == self.Role.ADMIN

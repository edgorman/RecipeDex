from enum import Enum
from uuid import UUID
from typing import Dict, Any
from dataclasses import dataclass, asdict

from starlette.authentication import BaseUser
from internal.config.auth import AuthProvider


class UserRole(Enum):
    UNDEFINED = "undefined"
    ADMIN = "admin"


@dataclass
class User(BaseUser):
    """Class for storing user information"""
    id: UUID
    name: str
    role: UserRole
    provider: AuthProvider
    provider_info: Dict[str, Any]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        def default(obj):
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, UserRole):
                return obj.value
            if isinstance(obj, AuthProvider):
                return obj.value
            if isinstance(obj, dict):
                return {default(k): default(v) for k, v in obj.items()}
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            id=UUID(data["id"]),
            name=data["name"],
            role=UserRole(data["role"]),
            provider=AuthProvider(data["provider"]),
            provider_info=data["provider_info"]
        )

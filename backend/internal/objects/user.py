from enum import Enum
from uuid import UUID
from typing import Any, Dict, Tuple
from dataclasses import dataclass, asdict, is_dataclass
from google.auth.transport import requests as token_request
from google.oauth2.id_token import verify_firebase_token
from starlette.authentication import BaseUser

from internal.config.service import Service


@dataclass
class User(BaseUser):
    """Object that stores user information"""
    id: UUID
    name: str
    role: "Role"
    provider: "Provider"
    deleted: bool = False

    class Role(Enum):
        UNDEFINED = "undefined"
        ADMIN = "admin"

    @dataclass
    class Provider:
        id: Any
        type: Service.AuthProvider
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

    def to_dict(self) -> dict:
        def default(obj):
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, User.Role):
                return obj.value
            if isinstance(obj, Service.AuthProvider):
                return obj.value
            if is_dataclass(obj):
                return default(asdict(obj))
            if isinstance(obj, dict):
                return {default(k): default(v) for k, v in obj.items()}
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            id=UUID(data["id"]),
            name=data["name"],
            role=User.Role(data["role"]),
            deleted=data["deleted"] if "deleted" in data else False,
            provider=User.Provider(
                id=data["provider"]["id"],
                type=data["provider"]["type"],
                info=data["provider"]["info"]
            )
        )

    @staticmethod
    def authenticate(provider: Service.AuthProvider, token: str, audience: Any) -> Tuple[Dict[str, Any], str, str]:
        match provider:
            case Service.AuthProvider.FIREBASE:
                info = verify_firebase_token(token, token_request.Request(), audience=audience)
                return info["user_id"], info["name"], info
            case _:
                raise NotImplementedError(f"Auth provider `{provider.name}` is not implemented")

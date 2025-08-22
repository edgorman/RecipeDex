from enum import Enum
from uuid import UUID
from typing import Any, Dict, List
from collections.abc import Iterable
from dataclasses import dataclass, asdict, is_dataclass
from starlette.authentication import BaseUser
from pydantic import TypeAdapter


@dataclass
class User(BaseUser):
    """Object that stores User information"""
    id: UUID
    name: str
    role: "Role"
    provider: "Provider"
    deleted: bool = False

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

    @dataclass
    class Provider:
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
    def from_dict(data: dict) -> "User":
        return TypeAdapter(User).validate_python(data)

    @classmethod
    def forbidden_keys_to_update(cls) -> List[str]:
        return ["id"]

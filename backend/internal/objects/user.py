import json
from typing import Dict, Any
from dataclasses import dataclass, asdict

from starlette.authentication import BaseUser
from internal.config.auth import AuthProvider


@dataclass
class User(BaseUser):
    """Class for storing user information"""
    id: str
    name: str
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
            if isinstance(obj, AuthProvider):
                return obj.value
            if isinstance(obj, dict):
                return {k: default(v) for k, v in obj.items()}
            if hasattr(obj, "__dict__"):
                return default(obj.__dict__)
            if hasattr(obj, "to_json"):
                return json.loads(obj.to_json())
            if hasattr(obj, "name"):
                return obj.name
            if hasattr(obj, "value"):
                return obj.value
            return obj

        return {k: default(v) for k, v in asdict(self).items()}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            id=data["id"],
            name=data["name"],
            provider=AuthProvider(data["provider"]),
            provider_info=data["provider_info"]
        )

    @staticmethod
    def from_json(data: str) -> "User":
        return User.from_dict(json.loads(data))

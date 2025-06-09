from typing import Dict, Any
from dataclasses import dataclass, asdict
import json

from internal.config.auth import AuthProvider


@dataclass
class User:
    """Class for storing user information"""
    id: str
    name: str
    provider: AuthProvider
    provider_info: Dict[str, Any]

    def to_json(self) -> str:
        def default(obj):
            if isinstance(obj, AuthProvider):
                return obj.value
            if hasattr(obj, "to_json"):
                return json.loads(obj.to_json())
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            if hasattr(obj, "name"):
                return obj.name
            if hasattr(obj, "value"):
                return obj.value
            return str(obj)
        return json.dumps(asdict(self), default=default)

    @staticmethod
    def from_json(data: str) -> "User":
        obj = json.loads(data)
        return User(
            id=obj["id"],
            name=obj["name"],
            provider=AuthProvider(obj["provider"]),
            provider_info=obj["provider_info"]
        )

from dataclasses import dataclass
from uuid import UUID

from internal.objects.user import User


@dataclass
class GetUserResponse:
    user_id: UUID
    user_name: str

    @classmethod
    def from_objects(cls, user: User) -> "GetUserResponse":
        """Create a GetUserResponse from a User object"""
        return cls(
            user_id=user.id,
            user_name=user.display_name
        )


@dataclass
class GetUserByProviderResponse:
    user_id: UUID
    user_name: str

    @classmethod
    def from_objects(cls, user: User) -> "GetUserByProviderResponse":
        """Create a GetUserByProviderResponse from a User object"""
        return cls(
            user_id=user.id,
            user_name=user.display_name
        )

from dataclasses import dataclass
from typing import Optional
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


@dataclass
class UpdateUserRequest:
    name: Optional[str] = None

    @classmethod
    def from_objects(cls, data: dict) -> "UpdateUserRequest":
        """Create an UpdateUserRequest from a dict object"""
        return cls(
            name=data.get("name")
        )


@dataclass
class UpdateUserResponse:
    user_id: UUID

    @classmethod
    def from_objects(cls, user: User) -> "UpdateUserResponse":
        """Create an UpdateUserResponse from a User object"""
        return cls(user_id=user.id)


@dataclass
class DeleteUserResponse:
    user_id: UUID

    @classmethod
    def from_objects(cls, user: User) -> "DeleteUserResponse":
        """Create a DeleteUserResponse from a User object"""
        return cls(user_id=user.id)

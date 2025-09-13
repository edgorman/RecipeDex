from abc import ABC, abstractmethod
from uuid import UUID
from typing import Any, Optional

from internal.objects.user import User


class UserStorage(ABC):
    """The UserStorage maintains user information in storage"""

    @abstractmethod
    def get(self, id_: UUID) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            id_: the ID of the user to get.

        Returns:
            the user if they exist, otherwise None.
        """
        ...

    @abstractmethod
    def get_by_provider_id(self, id_: Any, type_: User.ProviderType) -> Optional[User]:
        """
        Get a user by their provider ID.

        Args:
            id_: the provider ID of the user to get.
            type_: the provider type of the user to get.

        Returns:
            the user if they exist, otherwise None.
        """
        ...

    @abstractmethod
    def create(self, user: User) -> None:
        """
        Create a new user.

        Args:
            user: the user to create.
        """
        ...

    @abstractmethod
    def update(self, id_: UUID, user: User) -> None:
        """
        Update an existing user.

        Args:
            id_: the ID of the user to update.
            user: the user to update.
        """
        ...

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        """
        Delete a user.

        Args:
            id_: the ID of the user to delete.
        """
        ...

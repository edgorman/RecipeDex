import pytest
from uuid import uuid4
from datetime import datetime, timezone

from internal.objects.user import User


@pytest.fixture
def user() -> User:
    """Returns a basic User object."""
    return User(
        id=uuid4(),
        name="Test User",
        role=User.Role.ADMIN,
        provider=User.Provider(
            id="test_provider_id",
            type=User.ProviderType.FIREBASE,
            info={"email": "test@example.com"}
        )
    )


@pytest.mark.parametrize(
    "name, role, provider_type",
    [
        ("Test User 1", User.Role.ADMIN, User.ProviderType.FIREBASE),
        ("Another User", User.Role.UNDEFINED, User.ProviderType.UNDEFINED),
    ]
)
def test_user_creation(name: str, role: User.Role, provider_type: User.ProviderType):
    """
    Test that a User object can be created with different parameters.

    Args:
        name: the name of the user.
        role: the role of the user.
        provider_type: the provider type for the user.
    """
    user_id = uuid4()
    provider_id = "provider123"
    user = User(
        id=user_id,
        name=name,
        role=role,
        provider=User.Provider(
            id=provider_id,
            type=provider_type,
            info={}
        )
    )
    assert user.id == user_id
    assert user.name == name
    assert user.role == role
    assert user.provider.id == provider_id
    assert user.provider.type == provider_type
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert user.deleted_at is None


@pytest.mark.parametrize(
    "deleted_time, is_deleted_expected",
    [
        (None, False),
        (datetime.now(tz=timezone.utc), True),
    ]
)
def test_is_deleted(user: User, deleted_time: datetime, is_deleted_expected: bool):
    """
    Test the is_deleted property.

    Args:
        user: the user to test.
        deleted_time: the time the user was deleted.
        is_deleted_expected: the expected value of the is_deleted property.
    """
    user.deleted_at = deleted_time
    assert user.is_deleted == is_deleted_expected


def test_is_authenticated(user: User):
    """
    Test the is_authenticated property.

    Args:
        user: the user to test.
    """
    assert user.is_authenticated is True


def test_display_id(user: User):
    """
    Test the display_id property.

    Args:
        user: the user to test.
    """
    assert user.display_id == str(user.id)


def test_display_name(user: User):
    """
    Test the display_name property.

    Args:
        user: the user to test.
    """
    assert user.display_name == user.name


def test_provider_id(user: User):
    """
    Test the provider_id property.

    Args:
        user: the user to test.
    """
    assert user.provider_id == user.provider.id


@pytest.mark.parametrize(
    "role, can_call_expected",
    [
        (User.Role.ADMIN, True),
        (User.Role.UNDEFINED, False),
    ]
)
def test_can_call_generative_ai(user: User, role: User.Role, can_call_expected: bool):
    """
    Test the can_call_generative_ai property.

    Args:
        user: the user to test.
        role: the role to set for the user.
        can_call_expected: the expected value of the can_call_generative_ai property.
    """
    user.role = role
    assert user.can_call_generative_ai == can_call_expected


@pytest.mark.parametrize(
    "provider_id, provider_type, info",
    [
        ("firebase_user_1", User.ProviderType.FIREBASE, {"email": "a@b.com"}),
        ("12345", User.ProviderType.UNDEFINED, {}),
    ]
)
def test_provider_creation(provider_id: str, provider_type: User.ProviderType, info: dict):
    """
    Test that a Provider object can be created with different parameters.

    Args:
        provider_id: the ID of the provider.
        provider_type: the type of the provider.
        info: the info dictionary for the provider.
    """
    provider = User.Provider(id=provider_id, type=provider_type, info=info)
    assert provider.id == provider_id
    assert provider.type == provider_type
    assert provider.info == info

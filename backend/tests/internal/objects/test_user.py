import pytest
from datetime import datetime, timezone
from uuid import uuid4, UUID

from internal.objects.user import User


@pytest.fixture
def mock_user_dict():
    return {
        "id": str(uuid4()),
        "name": "Test User",
        "role": User.Role.UNDEFINED.value,
        "deleted": False,
        "provider": {
            "id": "mock_provider_id",
            "type": User.ProviderType.UNDEFINED.value,
            "info": {"email": "test@example.com"}
        },
        "created_at": datetime.now(tz=timezone.utc),
        "updated_at": datetime.now(tz=timezone.utc),
        "deleted_at": datetime.now(tz=timezone.utc),
    }


@pytest.fixture
def mock_user(mock_user_dict):
    return User(
        id=UUID(mock_user_dict["id"]),
        name=mock_user_dict["name"],
        role=User.Role(mock_user_dict["role"]),
        deleted=mock_user_dict["deleted"],
        provider=User.Provider(
            id=mock_user_dict["provider"]["id"],
            type=User.ProviderType(mock_user_dict["provider"]["type"]),
            info=mock_user_dict["provider"]["info"]
        ),
        created_at=mock_user_dict["created_at"],
        updated_at=mock_user_dict["updated_at"],
        deleted_at=mock_user_dict["deleted_at"],
    )


def test_to_dict(mock_user, mock_user_dict):
    assert mock_user.to_dict() == mock_user_dict


def test_from_dict(mock_user, mock_user_dict):
    user = User.from_dict(mock_user_dict)
    assert isinstance(user, User)
    assert user == mock_user

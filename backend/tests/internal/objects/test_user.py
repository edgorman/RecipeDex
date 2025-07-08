import pytest
from internal.objects.user import User, UserRole
from internal.config.auth import AuthProvider


@pytest.fixture
def mock_user_dict():
    return {
        "id": "123",
        "name": "Test User",
        "role": UserRole.UNDEFINED.value,
        "provider": AuthProvider.FIREBASE.value,
        "provider_info": {"email": "test@example.com"}
    }


@pytest.fixture
def mock_user(mock_user_dict):
    return User(
        id=mock_user_dict["id"],
        name=mock_user_dict["name"],
        role=UserRole(mock_user_dict["role"]),
        provider=AuthProvider(mock_user_dict["provider"]),
        provider_info=mock_user_dict["provider_info"]
    )


def test_to_dict(mock_user, mock_user_dict):
    assert mock_user.to_dict() == mock_user_dict


def test_from_dict(mock_user, mock_user_dict):
    user = User.from_dict(mock_user_dict)
    assert isinstance(user, User)
    assert user == mock_user

import json
import pytest
from internal.objects.user import User
from internal.config.auth import AuthProvider


@pytest.fixture
def mock_user_dict():
    return {
        "id": "123",
        "name": "Test User",
        "provider": AuthProvider.FIREBASE.value,
        "provider_info": {"email": "test@example.com"}
    }


@pytest.fixture
def mock_user(mock_user_dict):
    return User(
        id=mock_user_dict["id"],
        name=mock_user_dict["name"],
        provider=AuthProvider(mock_user_dict["provider"]),
        provider_info=mock_user_dict["provider_info"]
    )


def test_to_dict(mock_user, mock_user_dict):
    assert mock_user.to_dict() == mock_user_dict


def test_to_json(mock_user, mock_user_dict):
    json_str = mock_user.to_json()
    assert isinstance(json_str, str)
    assert json.loads(json_str) == mock_user_dict


def test_from_dict(mock_user, mock_user_dict):
    user = User.from_dict(mock_user_dict)
    assert isinstance(user, User)
    assert user == mock_user


def test_from_json(mock_user, mock_user_dict):
    user = User.from_json(json.dumps(mock_user_dict))
    assert isinstance(user, User)
    assert user == mock_user

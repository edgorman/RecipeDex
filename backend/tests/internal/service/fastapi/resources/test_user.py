import pytest
from unittest.mock import Mock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.auth import AuthProvider, AUTHENTICATED_SCOPE
from internal.objects.user import User, UserRole
from internal.service.fastapi.resources.user import UserResource


mock_user = User(
    id="mock_user_id",
    name="mock_name",
    role=UserRole.UNDEFINED,
    provider=AuthProvider.FIREBASE,
    provider_info={}
)


@pytest.fixture
def mock_user_storage_handler():
    return Mock()


@pytest.fixture
def mock_authenticate_backend():
    return Mock()


def awaitable_return(value):
    async def _inner(*args, **kwargs):
        return value
    return _inner


@pytest.fixture
def mock_endpoint():
    return "test_user_endpoint"


@pytest.fixture
def mock_client(mock_user_storage_handler, mock_authenticate_backend, mock_endpoint):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(UserResource(mock_user_storage_handler, mock_endpoint))
    return TestClient(api)


@pytest.mark.parametrize(
    "user_id,mock_get_auth,mock_get_user,expected_status,expected_content",
    [
        # User is authenticated, user exists, should allow
        (
            mock_user.id,
            (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            mock_user,
            200,
            {"id": mock_user.id, "display_name": "mock_name"}
        ),
        # User is authenticated, user does not exist, should allow
        (
            mock_user.id,
            (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            None,
            404,
            {"detail": f"Could not get user with id `{mock_user.id}`: `it does not exist`."}
        ),
        # User is not authenticated, user exists, should deny
        (
            mock_user.id,
            (None, UnauthenticatedUser()),
            mock_user,
            403,
            {"detail": f"Could not get user with id `{mock_user.id}`: `user is not authorized`."}
        ),
        # User is not authenticated, user does not exist, should deny
        (
            mock_user.id,
            (None, UnauthenticatedUser()),
            None,
            403,
            {"detail": f"Could not get user with id `{mock_user.id}`: `user is not authorized`."}
        ),
    ]
)
def test_get_user(
    mock_authenticate_backend,
    mock_client,
    mock_user_storage_handler,
    mock_endpoint,
    user_id,
    mock_get_auth,
    mock_get_user,
    expected_status,
    expected_content
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_user_storage_handler.get.return_value = mock_get_user

    try:
        response = mock_client.get(f"/{mock_endpoint}/{user_id}")
    except HTTPException as he:
        assert he.status_code == expected_status
        assert he.detail == expected_content
        return
    except Exception as e:
        assert False, f"Unexpected exception was thrown: {e}"

    assert response.status_code == expected_status
    assert response.json() == expected_content

import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import Mock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.service import SERVICE_AUTH_SCOPE
from internal.objects.user import User
from internal.service.fastapi.resources.user import UserResource


example_user = User(
    id=uuid4(),
    name="mock_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
        info={}
    )
)
example_deleted_user = User(
    id=uuid4(),
    name="mock_deleted_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
        info={}
    ),
    deleted_at=datetime.now()
)


@pytest.fixture
def example_user_storage_handler():
    return Mock()


@pytest.fixture
def mock_authenticate_backend():
    return Mock()


def awaitable_return(value):
    async def _inner(*args, **kwargs):
        return value
    return _inner


@pytest.fixture
def example_user_authorize_handler():
    return Mock()


@pytest.fixture
def mock_endpoint():
    return "test_user_endpoint"


@pytest.fixture
def mock_client(example_user_storage_handler, example_user_authorize_handler, mock_authenticate_backend, mock_endpoint):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(
        UserResource(
            example_user_storage_handler,
            example_user_authorize_handler,
            mock_endpoint
        )
    )
    return TestClient(api)


@pytest.mark.parametrize(
    "user_id,mock_get_auth,mock_get_user,mock_authorize_user,expected_status,expected_content",
    [
        # User is authenticated, user exists, should allow
        (
            example_user.id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_user, True,
            200,
            {
                "detail": "User get finished successfully.",
                "data": {
                    "id": example_user.display_id,
                    "name": example_user.display_name
                }
            }
        ),
        # User is authenticated, user does not exist, should allow
        (
            example_user.id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            None, True,
            404,
            {
                "detail": f"Could not get user with id `{example_user.display_id}`: `it does not exist`."
            }
        ),
        # User is not authenticated, user exists, should deny
        (
            example_user.id,
            (None, UnauthenticatedUser()),
            example_user, False,
            403,
            {"detail": f"Could not get user with id `{example_user.display_id}`: `user is forbidden`."}
        ),
        # User is not authenticated, user does not exist, should deny
        (
            example_user.id,
            (None, UnauthenticatedUser()),
            None, False,
            403,
            {"detail": f"Could not get user with id `{example_user.display_id}`: `user is forbidden`."}
        ),
        # User is deleted, should deny
        (
            example_deleted_user.id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_deleted_user),
            example_deleted_user, True,
            404,
            {"detail": f"Could not get user with id `{example_deleted_user.display_id}`: `it does not exist`."}
        ),
    ]
)
def test_get_user(
    mock_authenticate_backend,
    mock_client,
    example_user_storage_handler,
    example_user_authorize_handler,
    mock_endpoint,
    user_id,
    mock_get_auth,
    mock_get_user,
    mock_authorize_user,
    expected_status,
    expected_content
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    example_user_storage_handler.get.return_value = mock_get_user
    example_user_authorize_handler.authorize.return_value = mock_authorize_user

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

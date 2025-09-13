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
from internal.service.fastapi.schemas import BaseResponse
from internal.service.fastapi.schemas.user import GetUserResponse, UpdateUserResponse, DeleteUserResponse


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
def mock_user_authorize_handler():
    return Mock()


@pytest.fixture
def mock_endpoint():
    return "test_user_endpoint"


@pytest.fixture
def mock_client(mock_user_storage_handler, mock_user_authorize_handler, mock_authenticate_backend, mock_endpoint):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(
        UserResource(
            mock_user_storage_handler,
            mock_user_authorize_handler,
            mock_endpoint
        )
    )
    return TestClient(api)


@pytest.mark.parametrize(
    "user_id,mock_get_auth,mock_get_user,mock_authorize_user,expected_status,expected_content",
    [
        # User is authenticated, user exists, should allow
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, True, 200,
            BaseResponse(
                detail=f"User {User.Action.GET.value} finished successfully.",
                data=GetUserResponse.model_validate(example_user)
            ).model_dump(mode="json")
        ),
        # User is authenticated, user does not exist, should allow
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), None, True, 404,
            BaseResponse(
                detail=f"Could not {User.Action.GET.value} user with id `{example_user.display_id}`: "
                       f"`it does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is not authenticated, user exists, should deny
        (
            example_user.id, (None, UnauthenticatedUser()), example_user, False, 403,
            BaseResponse(
                detail=f"Could not {User.Action.GET.value} user with id `{example_user.display_id}`: "
                       f"`user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is not authenticated, user does not exist, should deny
        (
            example_user.id, (None, UnauthenticatedUser()), None, False, 403,
            BaseResponse(
                detail=f"Could not {User.Action.GET.value} user with id `{example_user.display_id}`: "
                       f"`user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is deleted, should deny
        (
            example_deleted_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_deleted_user),
            example_deleted_user, True, 404,
            BaseResponse(
                detail=f"Could not {User.Action.GET.value} user with id `{example_deleted_user.display_id}`: "
                       f"`it does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_get(
    mock_authenticate_backend,
    mock_client,
    mock_user_storage_handler,
    mock_user_authorize_handler,
    mock_endpoint,
    user_id,
    mock_get_auth,
    mock_get_user,
    mock_authorize_user,
    expected_status,
    expected_content
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_user_storage_handler.get.return_value = mock_get_user
    mock_user_authorize_handler.authorize.return_value = mock_authorize_user

    try:
        response = mock_client.get(f"/{mock_endpoint}/{user_id}")
    except HTTPException as he:
        assert he.status_code == expected_status
        assert he.detail == expected_content
        return
    except Exception as e:
        assert False, f"Unexpected exception was thrown: {e}"

    assert response.status_code == expected_status
    if expected_content.get("data") is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "provider,provider_id,mock_get_auth,mock_get_user,expected_status,expected_content",
    [
        # User is authenticated, user exists, should allow
        (
            example_user.provider.type.value, example_user.provider.id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, 200,
            BaseResponse(
                detail=f"User {User.Action.GET_BY_PROVIDER.value} finished successfully.",
                data=GetUserResponse.model_validate(example_user)
            ).model_dump(mode="json")
        ),
        # User is authenticated, user does not exist, should deny
        (
            example_user.provider.type.value, example_user.provider.id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), None, 404,
            BaseResponse(
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{example_user.provider.type.value}` and id "
                       f"`{example_user.provider.id}`: `user does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is not authenticated, should deny
        (
            example_user.provider.type.value, example_user.provider.id, (None, UnauthenticatedUser()), example_user,
            403, BaseResponse(
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{example_user.provider.type.value}` and id "
                       f"`{example_user.provider.id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Invalid provider, should deny
        (
            "invalid_provider", example_user.provider.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_user, 400,
            BaseResponse(
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `invalid_provider` and id "
                       f"`{example_user.provider.id}`: `invalid provider`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is deleted, should deny
        (
            example_deleted_user.provider.type.value, example_deleted_user.provider.id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_deleted_user), example_deleted_user, 404,
            BaseResponse(
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for "
                       f"`{example_deleted_user.provider.type.value}` and id `{example_deleted_user.provider.id}`: "
                       f"`user does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_get_by_provider_id(
    mock_authenticate_backend,
    mock_client,
    mock_user_storage_handler,
    mock_endpoint,
    provider,
    provider_id,
    mock_get_auth,
    mock_get_user,
    expected_status,
    expected_content
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_user_storage_handler.get_by_provider_id.return_value = mock_get_user

    response = mock_client.get(f"/{mock_endpoint}/provider/{provider}/{provider_id}")

    assert response.status_code == expected_status
    if expected_content.get("data") is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "user_id,mock_get_auth,mock_get_user,mock_authorize_user,request_body,expected_status,expected_content",
    [
        # Valid update
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, True,
            {"name": "Updated Name"}, 200,
            BaseResponse(
                detail=f"User {User.Action.UPDATE.value} finished successfully.",
                data=UpdateUserResponse(id=example_user.display_id, name="Updated Name")
            ).model_dump(mode="json")
        ),
        # Forbidden
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, False,
            {"name": "Updated Name"}, 403,
            BaseResponse(
                detail=f"Could not {User.Action.UPDATE.value} user with id `{example_user.display_id}`: "
                       f"`user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Not found
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), None, True,
            {"name": "Updated Name"}, 404,
            BaseResponse(
                detail=f"Could not {User.Action.UPDATE.value} user with id `{example_user.display_id}`: "
                       f"`it does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Invalid request body
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, True, {}, 400,
            BaseResponse(
                detail=f"Could not {User.Action.UPDATE.value} user: `all data fields cannot be null`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_update(
    mock_authenticate_backend,
    mock_client,
    mock_user_storage_handler,
    mock_user_authorize_handler,
    mock_endpoint,
    user_id,
    mock_get_auth,
    mock_get_user,
    mock_authorize_user,
    request_body,
    expected_status,
    expected_content
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_user_storage_handler.get.return_value = mock_get_user
    mock_user_authorize_handler.authorize.return_value = mock_authorize_user

    response = mock_client.put(f"/{mock_endpoint}/{user_id}", json={"data": request_body})

    assert response.status_code == expected_status
    if expected_content.get("data") is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "user_id,mock_get_auth,mock_get_user,mock_authorize_user,expected_status,expected_content",
    [
        # Valid delete
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, True, 200,
            BaseResponse(
                detail=f"User {User.Action.DELETE.value} finished successfully.",
                data=DeleteUserResponse.model_validate(example_user)
            ).model_dump(mode="json")
        ),
        # Forbidden
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), example_user, False, 403,
            BaseResponse(
                detail=f"Could not {User.Action.DELETE.value} user with id `{example_user.display_id}`: "
                       f"`user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Not found
        (
            example_user.id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), None, True, 404,
            BaseResponse(
                detail=f"Could not {User.Action.DELETE.value} user with id `{example_user.display_id}`: "
                       f"`it does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_delete(
    mock_authenticate_backend,
    mock_client,
    mock_user_storage_handler,
    mock_user_authorize_handler,
    mock_endpoint,
    user_id,
    mock_get_auth,
    mock_get_user,
    mock_authorize_user,
    expected_status,
    expected_content
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_user_storage_handler.get.return_value = mock_get_user
    mock_user_authorize_handler.authorize.return_value = mock_authorize_user

    response = mock_client.delete(f"/{mock_endpoint}/{user_id}")

    assert response.status_code == expected_status
    if expected_content.get("data") is None:
        del expected_content["data"]
    assert response.json() == expected_content

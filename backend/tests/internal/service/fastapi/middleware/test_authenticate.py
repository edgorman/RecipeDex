import pytest
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from internal.config.service import (
    Service,
    SERVICE_AUTH_HEADER,
    SERVICE_AUTH_PROVIDER_HEADER,
    SERVICE_AUTH_BEARER_PREFIX,
)
from internal.objects.user import User
from internal.service.fastapi.middleware.authenticate import add_authenticate_middleware


example_user = User(
    id="mock_id",
    name="mock_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=Service.AuthProvider.FIREBASE,
        info={}
    )
)


@pytest.fixture
def mock_user_handler():
    return Mock()


@pytest.fixture
def mock_client(mock_user_handler):
    api = FastAPI()
    add_authenticate_middleware(api, mock_user_handler)

    @api.get("/")
    async def root(request: Request):
        return JSONResponse(
            {
                "name": request.user.name if request.user.is_authenticated else None
            }
        )

    return TestClient(api)


@pytest.mark.parametrize(
    "mock_user_authenticate,mock_user_get,mock_user_create,headers,expected_status,expected_content",
    [
        # No header provided, allow access as unauthenticated user (resource not protected)
        (
            None, None, None, {}, 200, {"name": None}
        ),
        # Header malformed, prevent access with bad request error
        (
            None, None, None, {SERVICE_AUTH_HEADER: "blah"}, 400,
            f"`{SERVICE_AUTH_HEADER}` header malformed, must start with `{SERVICE_AUTH_BEARER_PREFIX}`."
        ),
        # Header malformed, prevent access with bad request error
        (
            None, None, None, {SERVICE_AUTH_HEADER: "Bearer blah"}, 400,
            f"`{SERVICE_AUTH_PROVIDER_HEADER}` is missing."
        ),
        # Header malformed, prevent access with bad request error
        (
            None, None, None,
            {SERVICE_AUTH_HEADER: f"{SERVICE_AUTH_BEARER_PREFIX}blah", SERVICE_AUTH_PROVIDER_HEADER: "blah"},
            400, f"`blah` is not a valid value for `{SERVICE_AUTH_PROVIDER_HEADER}`."
        ),
        # Mock authentication error, prevent access with internal server error
        (
            Exception("it exploded"), None, None,
            {
                SERVICE_AUTH_HEADER: f"{SERVICE_AUTH_BEARER_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            500, f"Could not authenticate with provider `{example_user.provider.type.value}`: `it exploded`."
        ),
        # Mock get user returns error, prevent access with internal server error
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            Exception("it exploded"), None,
            {
                SERVICE_AUTH_HEADER: f"{SERVICE_AUTH_BEARER_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            500, f"Could not get user for provider `{example_user.provider.type.value}`: `it exploded`."
        ),
        # Mock create user returns error, prevent access with internal server error
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            lambda _, __: None, Exception("it exploded"),
            {
                SERVICE_AUTH_HEADER: f"{SERVICE_AUTH_BEARER_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            500, f"Could not get user for provider `{example_user.provider.type.value}`: `it exploded`."
        ),
        # Valid header provided, allow access as authenticated user
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            lambda _, __: example_user, None,
            {
                SERVICE_AUTH_HEADER: f"{SERVICE_AUTH_BEARER_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            200, {"name": example_user.name}
        ),
    ]
)
def test_authenticate(
    mock_client,
    mock_user_handler,
    mock_user_authenticate,
    mock_user_get,
    mock_user_create,
    headers,
    expected_status,
    expected_content
):
    mock_user_handler.get_by_provider_id.side_effect = mock_user_get
    mock_user_handler.create.side_effect = mock_user_create

    with patch.object(User, "authenticate", side_effect=mock_user_authenticate):
        try:
            response = mock_client.get("/", headers=headers)
        except HTTPException as he:
            assert he.status_code == expected_status
            assert he.detail == expected_content
            return
        except Exception as e:
            assert False, f"Unexpected exception was thrown: {e}"

        assert response.status_code == expected_status
        assert response.json() == expected_content

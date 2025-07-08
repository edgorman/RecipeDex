import pytest
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from internal.config.auth import AuthProvider
from internal.objects.user import User, UserRole
from internal.service.fastapi.middleware.authenticate import (
    AuthenticateBackend, add_authenticate_middleware
)


mock_user = User(
    id="mock_id",
    name="mock_name",
    role=UserRole.UNDEFINED,
    provider=AuthProvider.FIREBASE,
    provider_info={}
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
            request.user.to_dict() if isinstance(request.user, User) else {"message": "success"}
        )

    return TestClient(api)


@pytest.mark.parametrize(
    "endpoint,headers,mock_auth_provider,mock_get_user,expected_status,expected_content",
    [
        (  # No auth in header is successful because user isn't trying to access protected resource
            "/", {}, None, None, 200, {"message": "success"}
        ),
        (  # Auth in header and successful authentication
            "/", {"Authorization": "Bearer blah", "Authorization-Provider": AuthProvider.FIREBASE.value},
            None, lambda _, __, ___: mock_user, 200, mock_user.to_dict()
        ),
        (  # Auth in header but no bearer token
            "/", {"Authorization": "blah"}, None, None, 400,
            "`Authorization` header malformed, must start with `Bearer `."
        ),
        (  # Bearer token in header but no provider
            "/", {"Authorization": "Bearer blah"}, None, None, 400,
            "`Authorization-Provider` is missing."
        ),
        (  # Provider in header but not a valid provider
            "/", {"Authorization": "Bearer blah", "Authorization-Provider": "blah"},
            None, None, 400, "`blah` is not a valid value for `Authorization-Provider`."
        ),
        (  # Valid provider but mock error on auth with provider
            "/", {"Authorization": "Bearer blah", "Authorization-Provider": AuthProvider.FIREBASE.value},
            Exception("it exploded"), None, 500,
            f"Could not authenticate with provider `{AuthProvider.FIREBASE.value}`: `it exploded`."
        ),
        (  # Valid auth with provider but mock error on get user
            "/", {"Authorization": "Bearer blah", "Authorization-Provider": AuthProvider.FIREBASE.value},
            None, Exception("it exploded"), 500,
            f"Could not get user for provider `{AuthProvider.FIREBASE.value}`: `it exploded`."
        )
    ]
)
def test_authenticate(
    mock_client, endpoint, headers, mock_auth_provider, mock_get_user, expected_status, expected_content
):
    with patch.object(AuthenticateBackend, "_auth_firebase", side_effect=mock_auth_provider):
        with patch.object(AuthenticateBackend, "_get_user", side_effect=mock_get_user):
            try:
                response = mock_client.get(endpoint, headers=headers)
            except HTTPException as he:
                assert he.status_code == expected_status
                assert he.detail == expected_content
                return
            except Exception as e:
                assert False, f"Unexpected exception was thrown: {e}"

            assert response.status_code == expected_status
            assert response.json() == expected_content

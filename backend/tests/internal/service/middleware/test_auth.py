import pytest
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from internal.config.auth import AuthProvider
from internal.objects.user import User
from internal.service.middleware.auth import (
    AuthBackend, add_auth_middleware, authenticate_request
)


mock_user = User(
    id="mock_id",
    name="mock_name",
    provider=AuthProvider.FIREBASE,
    provider_info={}
)


@pytest.fixture
def mock_user_handler():
    return Mock()


@pytest.fixture
def mock_client(mock_user_handler):
    app = FastAPI()
    add_auth_middleware(app, mock_user_handler)

    @app.get("/")
    async def root(request: Request):
        return JSONResponse(
            request.user.to_json() if isinstance(request.user, User) else {"message": "success"}
        )

    @app.get("/protected", dependencies=[Depends(authenticate_request)])
    async def protected(request: Request):
        return JSONResponse(request.user.to_json())

    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint,headers,mock_auth_provider,mock_get_user,expected_status,expected_content",
    [
        (  # No auth in header is successful because user isn't trying to access protected resource
            "/", {}, None, None, 200, {"message": "success"}
        ),
        (  # No auth in header and unsuccessful because user is trying to access protected resource
            "/protected", {}, None, None, 401, {"detail": "User must be authenticated for this endpoint."}
        ),
        (  # Auth in header and successful authentication
            "/", {"Authorization": "Bearer blah", "Authorization-Provider": AuthProvider.FIREBASE.value},
            None, lambda _, __: mock_user, 200, mock_user.to_json()
        ),
        (  # Auth in header and successful authentication with protected endpoint
            "/protected", {"Authorization": "Bearer blah", "Authorization-Provider": AuthProvider.FIREBASE.value},
            None, lambda _, __: mock_user, 200, mock_user.to_json()
        ),

        (  # Auth in header but no bearer token
            "/", {"Authorization": "blah"}, None, None, 400,
            "`Authorization` header malformed, must start with `Bearer `."
        ),
        (  # Bearer token in header but no provider
            "/", {"Authorization": "Bearer blah"}, None, None, 400, "`Authorization-Provider` is missing."
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
def test_auth_middleware(
    mock_client, endpoint, headers, mock_auth_provider, mock_get_user, expected_status, expected_content
):
    with patch.object(AuthBackend, "_auth_google", side_effect=mock_auth_provider):
        with patch.object(AuthBackend, "_get_user", side_effect=mock_get_user):
            headers |= {
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }

            try:
                response = mock_client.get(endpoint, headers=headers)
                assert response.status_code == expected_status
                assert response.json() == expected_content
            except HTTPException as he:
                assert he.status_code == expected_status
                assert he.detail == expected_content
            except Exception as e:
                assert False, f"Unexpected exception was thrown: {e}"

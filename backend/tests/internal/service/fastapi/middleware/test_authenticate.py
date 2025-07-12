import pytest
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket, WebSocketDisconnect
from unittest.mock import Mock, patch

from internal.config.service import (
    Service,
    SERVICE_AUTH_TOKEN_HEADER,
    SERVICE_AUTH_TOKEN_PREFIX,
    SERVICE_AUTH_PROVIDER_HEADER,
    SERVICE_AUTH_TOKEN_QUERY,
    SERVICE_AUTH_PROVIDER_QUERY
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

    @api.get("/http")
    async def http_endpoint(connection: Request):
        return JSONResponse(
            {
                "name": connection.user.name if connection.user.is_authenticated else None
            }
        )

    @api.websocket("/ws")
    async def websocket_endpoint(connection: WebSocket):
        await connection.accept()
        await connection.send_json(
            {
                "name": connection.user.name
            }
        )
        await connection.close()

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
            None, None, None, {SERVICE_AUTH_TOKEN_HEADER: "blah"}, 400,
            {
                "detail": "Could not parse authentication parameters: header is malformed, "
                          f"`{SERVICE_AUTH_TOKEN_HEADER}` must start with `{SERVICE_AUTH_TOKEN_PREFIX}`."
            }
        ),
        # Header malformed, prevent access with bad request error
        (
            None, None, None, {SERVICE_AUTH_TOKEN_HEADER: "Bearer blah"}, 400,
            {
                "detail": "Could not parse authentication parameters: "
                          f"header is malformed, must include `{SERVICE_AUTH_PROVIDER_HEADER}`."
            }
        ),
        # Header malformed, prevent access with bad request error
        (
            None, None, None,
            {
                SERVICE_AUTH_TOKEN_HEADER: f"{SERVICE_AUTH_TOKEN_PREFIX}blah", SERVICE_AUTH_PROVIDER_HEADER: "blah"
            }, 400, {"detail": "Could not parse authentication parameters: `blah` is invalid."}
        ),
        # Mock authentication error, prevent access with internal server error
        (
            Exception("it exploded"), None, None,
            {
                SERVICE_AUTH_TOKEN_HEADER: f"{SERVICE_AUTH_TOKEN_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            500, {"detail": "Could not authenticate, internal error: it exploded."}
        ),
        # Mock get user returns error, prevent access with internal server error
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            Exception("it exploded"), None,
            {
                SERVICE_AUTH_TOKEN_HEADER: f"{SERVICE_AUTH_TOKEN_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            500, {"detail": "Could not get user, internal error: it exploded."}
        ),
        # Mock create user returns error, prevent access with internal server error
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            lambda _, __: None, Exception("it exploded"),
            {
                SERVICE_AUTH_TOKEN_HEADER: f"{SERVICE_AUTH_TOKEN_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            500, {"detail": "Could not get user, internal error: it exploded."}
        ),
        # Valid header provided, allow access as authenticated user
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            lambda _, __: example_user, None,
            {
                SERVICE_AUTH_TOKEN_HEADER: f"{SERVICE_AUTH_TOKEN_PREFIX}blah",
                SERVICE_AUTH_PROVIDER_HEADER: example_user.provider.type.value
            },
            200, {"name": example_user.name}
        ),
    ]
)
def test_authenticate_http(
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
            response = mock_client.get("/http", headers=headers)
        except Exception as e:
            assert False, f"Unexpected exception was thrown: {e}"

        assert response.status_code == expected_status
        assert response.json() == expected_content


@pytest.mark.parametrize(
    "mock_user_authenticate,mock_user_get,mock_user_create,query_params,expected_status,expected_message",
    [
        # Query malformed, prevent access with bad request error
        (
            None, None, None, "", status.WS_1008_POLICY_VIOLATION,
            "Could not parse authentication parameters: "
            f"header is malformed, must include `{SERVICE_AUTH_TOKEN_QUERY}`."
        ),
        # Query malformed, prevent access with bad request error
        (
            None, None, None, f"?{SERVICE_AUTH_TOKEN_QUERY}=blah", status.WS_1008_POLICY_VIOLATION,
            "Could not parse authentication parameters: "
            f"header is malformed, must include `{SERVICE_AUTH_PROVIDER_QUERY}`."
        ),
        # Valid query provided, allow access as authenticated user
        (
            lambda _, __, ___: (example_user.provider_id, example_user.name, example_user.provider.info),
            lambda _, __: example_user, None,
            f"?{SERVICE_AUTH_TOKEN_QUERY}={SERVICE_AUTH_TOKEN_PREFIX}blah"
            f"&{SERVICE_AUTH_PROVIDER_QUERY}={example_user.provider.type.value}",
            status.WS_1000_NORMAL_CLOSURE, {"name": example_user.name}
        )
    ]
)
def test_authenticate_websocket(
    mock_client,
    mock_user_handler,
    mock_user_authenticate,
    mock_user_get,
    mock_user_create,
    query_params,
    expected_status,
    expected_message
):
    mock_user_handler.get_by_provider_id.side_effect = mock_user_get
    mock_user_handler.create.side_effect = mock_user_create

    with patch.object(User, "authenticate", side_effect=mock_user_authenticate):
        try:
            with mock_client.websocket_connect(f"/ws{query_params}") as websocket:
                message = websocket.receive_json()
                assert message == expected_message
        except WebSocketDisconnect as e:
            assert e.code == expected_status
        except Exception as e:
            assert False, f"Unexpected exception: {e}"

from uuid import uuid4
from typing import Tuple
from fastapi import FastAPI, status, Request, HTTPException
from starlette.authentication import AuthenticationBackend, AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket

from internal.config.service import (
    Service,
    SERVICE_AUTH_SCOPE,
    SERVICE_AUTH_TOKEN_HEADER,
    SERVICE_AUTH_TOKEN_PREFIX,
    SERVICE_AUTH_PROVIDER_HEADER,
    SERVICE_AUTH_TOKEN_QUERY,
    SERVICE_AUTH_PROVIDER_QUERY,
    SERVICE_PROJECT_ID
)
from internal.objects.user import User
from internal.storage.user import UserStorage


class AuthenticationAsyncMiddleware(AuthenticationMiddleware):
    """Async version of `starlette.middleware.authentication.AuthenticationMiddleware`"""

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        try:
            auth_result = await self.backend.authenticate(conn)
        except HTTPException as he:
            if scope["type"] == "websocket":
                try:
                    await send({"type": "websocket.send", "detail": he.detail})
                    await send({"type": "websocket.close", "code": he.status_code})
                except Exception:
                    await send({"type": "websocket.close", "code": status.WS_1011_INTERNAL_ERROR})
            else:
                response = JSONResponse({"detail": he.detail}, he.status_code)
                await response(scope, receive, send)
            return

        if auth_result is None:
            auth_result = AuthCredentials(), UnauthenticatedUser()
        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)


class AuthenticateBackend(AuthenticationBackend):
    def __init__(self, user_storage_handler: UserStorage):
        self.__user_storage_handler = user_storage_handler

    async def authenticate(self, connection: HTTPConnection) -> Tuple[AuthCredentials, User] | None:
        try:
            if connection.get("type") == "websocket":
                provider, token = await self._parse_websocket_parameters(connection)
            else:
                provider, token = await self._parse_http_headers(connection)
                if provider is None and token is None:
                    return
        except HTTPException as he:
            raise HTTPException(
                he.status_code, f"Could not parse authentication parameters: {he.detail}."
            )

        try:
            provider_type = Service.AuthProvider(provider)
        except ValueError:
            code = status.HTTP_400_BAD_REQUEST
            if isinstance(connection, WebSocket):
                code = status.WS_1008_POLICY_VIOLATION

            raise HTTPException(
                code, f"Could not parse authentication parameters: `{provider}` is invalid."
            )

        try:
            provider_id, provider_name, provider_info = User.authenticate(provider_type, token, SERVICE_PROJECT_ID)
        except Exception as e:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if isinstance(connection, WebSocket):
                code = status.WS_1011_INTERNAL_ERROR

            raise HTTPException(
                code, f"Could not authenticate, internal error: {e}."
            )

        try:
            user = self.__user_storage_handler.get_by_provider_id(provider_id, provider_type)

            # if no user is found, create one
            if user is None:
                user = User(
                    id=uuid4(),
                    name=provider_name,
                    role=User.Role.UNDEFINED,
                    provider=User.Provider(
                        id=provider_id,
                        type=provider_type,
                        info=provider_info
                    )
                )
                self.__user_storage_handler.create(user)

        except Exception as e:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if isinstance(connection, WebSocket):
                code = status.WS_1011_INTERNAL_ERROR

            raise HTTPException(
                code, f"Could not get user, internal error: {e}."
            )

        return AuthCredentials([SERVICE_AUTH_SCOPE]), user

    async def _parse_http_headers(self, connection: Request) -> Tuple[str, str]:
        if SERVICE_AUTH_TOKEN_HEADER not in connection.headers:
            return None, None  # allow requests that have no authentication
        auth = connection.headers[SERVICE_AUTH_TOKEN_HEADER]

        if not auth.startswith(SERVICE_AUTH_TOKEN_PREFIX):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"header is malformed, `{SERVICE_AUTH_TOKEN_HEADER}` must start with `{SERVICE_AUTH_TOKEN_PREFIX}`"
            )
        token = auth.split(SERVICE_AUTH_TOKEN_PREFIX)[1]

        if SERVICE_AUTH_PROVIDER_HEADER not in connection.headers:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"header is malformed, must include `{SERVICE_AUTH_PROVIDER_HEADER}`"
            )
        provider = connection.headers[SERVICE_AUTH_PROVIDER_HEADER]

        return provider, token

    async def _parse_websocket_parameters(self, connection: WebSocket) -> Tuple[str, str]:
        if SERVICE_AUTH_TOKEN_QUERY not in connection.query_params:
            raise HTTPException(
                status.WS_1008_POLICY_VIOLATION,
                f"query is malformed, must include `{SERVICE_AUTH_TOKEN_QUERY}`"
            )
        auth = connection.query_params[SERVICE_AUTH_TOKEN_QUERY]

        if not auth.startswith(SERVICE_AUTH_TOKEN_PREFIX):
            raise HTTPException(
                status.WS_1008_POLICY_VIOLATION,
                f"query is malformed, `{SERVICE_AUTH_TOKEN_QUERY}` must start with `{SERVICE_AUTH_TOKEN_PREFIX}`"
            )
        token = auth.split(SERVICE_AUTH_TOKEN_PREFIX)[1]

        if SERVICE_AUTH_PROVIDER_QUERY not in connection.query_params:
            raise HTTPException(
                status.WS_1008_POLICY_VIOLATION,
                f"query is malformed, must include `{SERVICE_AUTH_PROVIDER_QUERY}`"
            )
        provider = connection.query_params[SERVICE_AUTH_PROVIDER_QUERY]

        return provider, token


def add_authenticate_middleware(
    app: FastAPI,
    user_storage_handler: UserStorage,
):
    backend = AuthenticateBackend(user_storage_handler=user_storage_handler)
    app.add_middleware(AuthenticationAsyncMiddleware, backend=backend)

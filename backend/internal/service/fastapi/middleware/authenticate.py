from uuid import uuid4
from fastapi import FastAPI, HTTPException
from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response

from internal.config.gcp import PROJECT_ID as GCP_PROJECT_ID
from internal.config.auth import (
    AuthProvider, AUTHENTICATED_SCOPE, AUTHORIZATION_HEADER, AUTHORIZATION_BEARER_PREFIX, AUTHORIZATION_PROVIDER_HEADER
)
from internal.objects.user import User
from internal.storage.user import UserStorage


class AuthenticateBackend(AuthenticationBackend):
    def __init__(self, user_storage_handler: UserStorage):
        self.__user_storage_handler = user_storage_handler

    async def authenticate(self, connection: HTTPConnection) -> tuple[AuthCredentials, User] | None:
        if AUTHORIZATION_HEADER not in connection.headers:
            return

        auth = connection.headers[AUTHORIZATION_HEADER]
        if not auth.startswith(AUTHORIZATION_BEARER_PREFIX):
            raise HTTPException(
                status_code=400,
                detail=f"`{AUTHORIZATION_HEADER}` header malformed, must start with `{AUTHORIZATION_BEARER_PREFIX}`."
            )
        token = auth.split(AUTHORIZATION_BEARER_PREFIX)[1]

        if AUTHORIZATION_PROVIDER_HEADER not in connection.headers:
            raise HTTPException(status_code=400, detail=f"`{AUTHORIZATION_PROVIDER_HEADER}` is missing.")

        try:
            provider_type = AuthProvider(connection.headers[AUTHORIZATION_PROVIDER_HEADER])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"`{connection.headers[AUTHORIZATION_PROVIDER_HEADER]}` is not a valid value for "
                       f"`{AUTHORIZATION_PROVIDER_HEADER}`."
            )

        try:
            provider_id, provider_name, provider_info = User.authenticate(provider_type, token, GCP_PROJECT_ID)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Could not authenticate with provider `{provider_type.value}`: `{e}`."
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
            raise HTTPException(
                status_code=500,
                detail=f"Could not get user for provider `{provider_type.value}`: `{e}`."
            )

        return AuthCredentials([AUTHENTICATED_SCOPE]), user

    def on_error(connection: HTTPConnection, exception: HTTPException) -> Response:
        return JSONResponse(status_code=exception.status_code, content={"detail": str(exception.detail)})


def add_authenticate_middleware(
    app: FastAPI,
    user_storage_handler: UserStorage,
):
    backend = AuthenticateBackend(user_storage_handler=user_storage_handler)
    app.add_middleware(AuthenticationMiddleware, backend=backend, on_error=backend.on_error)

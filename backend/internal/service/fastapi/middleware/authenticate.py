from fastapi import FastAPI, HTTPException
from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response

from google.auth.transport import requests as firebase_request
from google.oauth2.id_token import verify_firebase_token

from internal.config.gcp import PROJECT_ID as GCP_PROJECT_ID
from internal.config.auth import (
    AuthProvider, AUTHENTICATED_SCOPE, AUTHORIZATION_HEADER, AUTHORIZATION_BEARER_PREFIX, AUTHORIZATION_PROVIDER_HEADER
)
from internal.objects.user import User
from internal.storage.user import UserStorage


class AuthenticateBackend(AuthenticationBackend):
    def __init__(self, user_handler):
        self.__user_handler = user_handler

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
            provider = AuthProvider(connection.headers[AUTHORIZATION_PROVIDER_HEADER])
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"`{connection.headers[AUTHORIZATION_PROVIDER_HEADER]}` is not a valid value for "
                       f"`{AUTHORIZATION_PROVIDER_HEADER}`."
            )

        try:
            match provider:
                case AuthProvider.FIREBASE:
                    provider_data = self._auth_google(token)
                case _:
                    raise NotImplementedError("Provider has not been implemented.")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Could not authenticate with provider `{provider.value}`: `{e}`."
            )

        try:
            user = self._get_user(provider, provider_data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not get user for provider `{provider.value}`: `{e}`."
            )

        return AuthCredentials([AUTHENTICATED_SCOPE]), user

    def _auth_google(self, token: str) -> dict:
        data = verify_firebase_token(
            token, firebase_request.Request(), audience=GCP_PROJECT_ID
        )
        if not data:
            raise Exception("invalid token")

        return data

    def _get_user(self, provider: AuthProvider, provider_data: dict) -> User:
        return User(
            id=provider_data["user_id"],
            name=provider_data["name"],
            provider=provider,
            provider_info=provider_data
        )

        # TODO: when user handler has been implemented
        # user = self.__user_handler.get_user_by_auth_provider(provider, provider_data)
        # if user is None:
        #     user = self.__user_handler.create_user_from_auth_provider(provider, provider_data)
        # return user

    def on_error(connection: HTTPConnection, exception: HTTPException) -> Response:
        return JSONResponse(status_code=exception.status_code, content={"detail": str(exception.detail)})


def add_authenticate_middleware(
    app: FastAPI,
    user_handler: UserStorage,
):
    backend = AuthenticateBackend(user_handler=user_handler)
    app.add_middleware(AuthenticationMiddleware, backend=backend, on_error=backend.on_error)

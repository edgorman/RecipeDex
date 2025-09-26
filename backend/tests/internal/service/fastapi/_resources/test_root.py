import pytest
from uuid import uuid4
from unittest.mock import Mock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.service import SERVICE_AUTH_SCOPE
from internal.objects.user import User
from internal.service.fastapi._resources.root import RootResource
from internal.service._schemas import BaseResponse
from internal.service._schemas.root import GetRootResponse


example_user = User(
    id=uuid4(),
    name="example_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
        info={}
    )
)


example_name = "example_name"
example_version = "example_version"


@pytest.fixture
def mock_authenticate_backend():
    return Mock()


def awaitable_return(value):
    async def _inner(*args, **kwargs):
        return value
    return _inner


@pytest.fixture
def mock_client(mock_authenticate_backend):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(
        RootResource(
            example_name,
            example_version
        )
    )

    return TestClient(api)


@pytest.mark.parametrize(
    "mock_get_auth,expected_status,expected_content",
    [
        # User is authenticated
        (
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), 200,
            BaseResponse(
                detail="Root get finished successfully.",
                data=GetRootResponse(
                    name=example_name,
                    version=example_version,
                    message="Welcome back example_name :)"
                )
            ).model_dump(mode="json")
        ),
        # User is not authenticated
        (
            (None, UnauthenticatedUser()), 200,
            BaseResponse(
                detail="Root get finished successfully.",
                data=GetRootResponse(name=example_name, version=example_version, message="Hello World :)")
            ).model_dump(mode="json")
        )
    ]
)
def test_get(
    mock_authenticate_backend,
    mock_client,
    mock_get_auth,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    response = mock_client.get("/")

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content

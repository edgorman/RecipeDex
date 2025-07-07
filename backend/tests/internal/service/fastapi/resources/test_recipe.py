import pytest
from unittest.mock import Mock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.auth import AuthProvider, AUTHENTICATED_SCOPE
from internal.objects.user import User
from internal.objects.recipe import Recipe
from internal.service.fastapi.resources.recipe import RecipeResource, RECIPE_RESOURCE_ENDPOINT


mock_recipe_public_no_acl = Recipe("mock_recipe_id", private=False, user_access_mapping={})


@pytest.fixture
def mock_user():
    return User(
        id="mock_user_id",
        name="mock_name",
        provider=AuthProvider.FIREBASE,
        provider_info={}
    )


@pytest.fixture
def mock_recipe_storage_handler():
    return Mock()


@pytest.fixture
def mock_recipe_agent_handler():
    return Mock()


@pytest.fixture
def mock_authenticate_backend():
    return Mock()


def awaitable_return(value):
    async def _inner(*args, **kwargs):
        return value
    return _inner


@pytest.fixture
def mock_client(mock_user, mock_recipe_storage_handler, mock_recipe_agent_handler, mock_authenticate_backend):
    api = FastAPI()
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(
        (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user)
    )
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(RecipeResource(mock_recipe_storage_handler, mock_recipe_agent_handler))

    return TestClient(api)


@pytest.mark.parametrize(
    "recipe_id,mock_get_recipe,expected_status,expected_content",
    [
        (
            "mock_recipe_id", mock_recipe_public_no_acl, 200,
            {"detail": "Recipe get finished successfully.", "recipe": mock_recipe_public_no_acl.to_json()}
        )
    ]
)
def test_get(
    mock_client, recipe_id, mock_get_recipe,  expected_status, expected_content, mock_recipe_storage_handler
):
    mock_recipe_storage_handler.get.return_value = mock_get_recipe

    try:
        response = mock_client.get(f"/{RECIPE_RESOURCE_ENDPOINT}/{recipe_id}")
    except HTTPException as he:
        assert he.status_code == expected_status
        assert he.detail == expected_content
        return
    except Exception as e:
        assert False, f"Unexpected exception was thrown: {e}"

    breakpoint()
    assert response.status_code == expected_status
    assert response.json() == expected_content

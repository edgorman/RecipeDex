import pytest
from uuid import uuid4
from unittest.mock import Mock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.auth import AuthProvider, AUTHENTICATED_SCOPE
from internal.objects.user import User, UserRole
from internal.objects.recipe import Recipe, RecipeRole
from internal.service.fastapi.resources.recipe import RecipeResource


mock_user = User(
    id="mock_user_id",
    name="mock_name",
    role=UserRole.UNDEFINED,
    provider=AuthProvider.UNDEFINED,
    provider_info={}
)
mock_recipe_public_no_acl = Recipe(uuid4(), private=False, user_access_mapping={})
mock_recipe_private_no_acl = Recipe(uuid4(), private=True, user_access_mapping={})
mock_recipe_private_with_viewer = Recipe(
    uuid4(), private=True, user_access_mapping={"mock_user_id": RecipeRole.VIEWER}
)
mock_recipe_public_with_viewer = Recipe(
    uuid4(), private=False, user_access_mapping={"mock_user_id": RecipeRole.VIEWER}
)
mock_recipe_private_with_undefined = Recipe(
    uuid4(), private=True, user_access_mapping={"mock_user_id": RecipeRole.UNDEFINED}
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
def mock_endpoint():
    return "test_recipe_endpoint"


@pytest.fixture
def mock_client(
    mock_recipe_storage_handler, mock_recipe_agent_handler, mock_authenticate_backend, mock_endpoint
):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(RecipeResource(mock_recipe_storage_handler, mock_recipe_agent_handler, mock_endpoint))

    return TestClient(api)


@pytest.mark.parametrize(
    "recipe_id,mock_get_auth,mock_get_recipe,expected_status,expected_content",
    [
        # User is authenticated, public recipe, no ACL, should allow
        (
            str(mock_recipe_public_no_acl.id), (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            mock_recipe_public_no_acl, 200,
            {"detail": "Recipe get finished successfully.", "recipe": {"id": str(mock_recipe_public_no_acl.id)}}
        ),
        # User is authenticated, private recipe, no ACL, should deny
        (
            str(mock_recipe_private_no_acl.id), (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            mock_recipe_private_no_acl, 403,
            {
                "detail": f"Could not get recipe with id `{str(mock_recipe_private_no_acl.id)}`: "
                "`user is not authorized`."
            }
        ),
        # User is authenticated, public recipe, allow VIEWER user, should allow
        (
            str(mock_recipe_public_with_viewer.id), (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            mock_recipe_public_with_viewer, 200,
            {"detail": "Recipe get finished successfully.", "recipe": {"id": str(mock_recipe_public_with_viewer.id)}}
        ),
        # User is authenticated, private recipe, allow VIEWER user, should allow
        (
            str(mock_recipe_private_with_viewer.id), (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            mock_recipe_private_with_viewer, 200,
            {"detail": "Recipe get finished successfully.", "recipe": {"id": str(mock_recipe_private_with_viewer.id)}}
        ),
        # User is authenticated, private recipe, allow UNDEFINED user, should deny
        (
            str(mock_recipe_private_with_undefined.id), (AuthCredentials([AUTHENTICATED_SCOPE]), mock_user),
            mock_recipe_private_with_undefined, 403,
            {
                "detail": f"Could not get recipe with id `{str(mock_recipe_private_with_undefined.id)}`: "
                "`user is not authorized`."
            }
        ),
        # User is not authenticated, public recipe, allow VIEWER user, should allow
        (
            str(mock_recipe_public_with_viewer.id), (None, UnauthenticatedUser()),
            mock_recipe_public_with_viewer, 200,
            {"detail": "Recipe get finished successfully.", "recipe": {"id": str(mock_recipe_public_with_viewer.id)}}
        ),
        # User is not authenticated, private recipe, allow VIEWER user, should deny
        (
            str(mock_recipe_private_with_viewer.id), (None, UnauthenticatedUser()),
            mock_recipe_private_with_viewer, 403,
            {
                "detail": f"Could not get recipe with id `{str(mock_recipe_private_with_viewer.id)}`: "
                "`user is not authorized`."
            }
        ),
    ]
)
def test_get(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.get.return_value = mock_get_recipe

    try:
        response = mock_client.get(f"/{mock_endpoint}/{recipe_id}")
    except HTTPException as he:
        assert he.status_code == expected_status
        assert he.detail == expected_content
        return
    except Exception as e:
        assert False, f"Unexpected exception was thrown: {e}"

    assert response.status_code == expected_status
    assert response.json() == expected_content

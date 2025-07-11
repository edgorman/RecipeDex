import pytest
from uuid import uuid4
from unittest.mock import Mock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.service import Service, SERVICE_AUTH_SCOPE
from internal.objects.user import User
from internal.objects.recipe import Recipe
from internal.service.fastapi.resources.recipe import RecipeResource


example_user = User(
    id=uuid4(),
    name="mock_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=Service.AuthProvider.UNDEFINED,
        info={}
    )
)

example_deleted_recipe = Recipe(uuid4(), name="mock_recipe", deleted=True)
example_public_recipe = Recipe(uuid4(), name="mock_recipe", private=False)
example_private_recipe = Recipe(uuid4(), name="mock_recipe", private=True)

example_private_with_viewer_recipe = Recipe(
    uuid4(), name="mock_recipe", private=True, user_access_mapping={example_user.id: Recipe.Role.VIEWER}
)
example_public_with_viewer_recipe = Recipe(
    uuid4(), name="mock_recipe", private=False, user_access_mapping={example_user.id: Recipe.Role.VIEWER}
)
example_private_with_undefined_recipe = Recipe(
    uuid4(), name="mock_recipe", private=True, user_access_mapping={example_user.id: Recipe.Role.UNDEFINED}
)


@pytest.fixture
def example_storage_handler_recipe():
    return Mock()


@pytest.fixture
def example_agent_handler_recipe():
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
    example_storage_handler_recipe, example_agent_handler_recipe, mock_authenticate_backend, mock_endpoint
):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(RecipeResource(example_storage_handler_recipe, example_agent_handler_recipe, mock_endpoint))

    return TestClient(api)


@pytest.mark.parametrize(
    "recipe_id,mock_get_auth,mock_get_recipe,expected_status,expected_content",
    [
        # User is authenticated, public recipe, no ACL, should allow
        (
            example_public_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, 200,
            {"detail": "Recipe get finished successfully.", "recipe": {"id": example_public_recipe.display_id}}
        ),
        # User is authenticated, private recipe, no ACL, should deny
        (
            example_private_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_recipe, 403,
            {
                "detail": f"Could not get recipe with id `{example_private_recipe.display_id}`: "
                "`user is not authorized`."
            }
        ),
        # User is authenticated, public recipe, allow VIEWER user, should allow
        (
            example_public_with_viewer_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_with_viewer_recipe, 200,
            {
                "detail": "Recipe get finished successfully.",
                "recipe": {"id": example_public_with_viewer_recipe.display_id}
            }
        ),
        # User is authenticated, private recipe, allow VIEWER user, should allow
        (
            example_private_with_viewer_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_with_viewer_recipe, 200,
            {
                "detail": "Recipe get finished successfully.",
                "recipe": {"id": example_private_with_viewer_recipe.display_id}
            }
        ),
        # User is authenticated, private recipe, allow UNDEFINED user, should deny
        (
            example_private_with_undefined_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_with_undefined_recipe, 403,
            {
                "detail": f"Could not get recipe with id `{example_private_with_undefined_recipe.display_id}`: "
                "`user is not authorized`."
            }
        ),
        # User is not authenticated, public recipe, allow VIEWER user, should allow
        (
            example_public_with_viewer_recipe.display_id, (None, UnauthenticatedUser()),
            example_public_with_viewer_recipe, 200,
            {
                "detail": "Recipe get finished successfully.",
                "recipe": {"id": example_public_with_viewer_recipe.display_id}
            }
        ),
        # User is not authenticated, private recipe, allow VIEWER user, should deny
        (
            example_private_with_viewer_recipe.display_id, (None, UnauthenticatedUser()),
            example_private_with_viewer_recipe, 403,
            {
                "detail": f"Could not get recipe with id `{example_private_with_viewer_recipe.display_id}`: "
                "`user is not authorized`."
            }
        ),
        # Recipe is deleted, should deny
        (
            example_deleted_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_deleted_recipe, 404,
            {"detail": f"Could not get recipe with id `{example_deleted_recipe.display_id}`: `it does not exist`."}
        )
    ]
)
def test_get(
    mock_authenticate_backend,
    mock_client,
    example_storage_handler_recipe,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    example_storage_handler_recipe.get.return_value = mock_get_recipe

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

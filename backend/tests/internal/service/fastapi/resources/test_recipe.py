import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import Mock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware

from internal.config.service import SERVICE_AUTH_SCOPE
from internal.objects.user import User
from internal.objects.recipe import Recipe
from internal.service.fastapi.resources.recipe import RecipeResource
from internal.service.fastapi.schemas import BaseRequest, BaseResponse
from internal.service.fastapi.schemas.recipe import (
    ListRecipesItem, ListRecipesResponse, GetRecipeResponse, GetMetadataResponse, CreateRecipeRequest,
    UpdateRecipeRequest, UpdateRecipeResponse, DeleteRecipeResponse, GetMessagesItem, GetMessagesResponse,
    CreateRecipeResponse
)


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
example_admin_user = User(
    id=uuid4(),
    name="example_admin_name",
    role=User.Role.ADMIN,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
        info={}
    )
)

example_deleted_recipe = Recipe(id=uuid4(), name="example_deleted_recipe", deleted_at=datetime.now())
example_public_recipe = Recipe(id=uuid4(), name="example_public_recipe", private=False)
example_private_recipe = Recipe(id=uuid4(), name="example_private_recipe", private=True)

example_private_with_viewer_recipe = Recipe(
    id=uuid4(),
    name="example_private_with_viewer_recipe",
    private=True,
    user_role_mapping={example_user.id: Recipe.Role.VIEWER}
)
example_public_with_viewer_recipe = Recipe(
    id=uuid4(),
    name="example_public_with_viewer_recipe",
    private=False,
    user_role_mapping={example_user.id: Recipe.Role.VIEWER}
)
example_private_with_undefined_recipe = Recipe(
    id=uuid4(),
    name="example_private_with_undefined_recipe",
    private=True,
    user_role_mapping={example_user.id: Recipe.Role.UNDEFINED}
)

example_messages = [Recipe.Message(role=Recipe.Message.Role.USER, value="example_value")]
example_nonexistent_id = uuid4()


@pytest.fixture
def mock_recipe_storage_handler():
    return Mock()


@pytest.fixture
def mock_recipe_agent_handler():
    return Mock()


@pytest.fixture
def mock_recipe_authorize_handler():
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
    mock_recipe_storage_handler,
    mock_recipe_agent_handler,
    mock_recipe_authorize_handler,
    mock_authenticate_backend,
    mock_endpoint
):
    api = FastAPI()
    api.add_middleware(AuthenticationMiddleware, backend=mock_authenticate_backend)
    api.include_router(
        RecipeResource(
            mock_recipe_storage_handler,
            mock_recipe_agent_handler,
            mock_recipe_authorize_handler,
            mock_endpoint
        )
    )

    return TestClient(api)


@pytest.mark.parametrize(
    "mock_get_auth,mock_list_recipes,mock_authorize_user,expected_status,expected_content",
    [
        # User is authenticated, should see all recipes they are authorized for
        (
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            [example_public_recipe, example_private_with_viewer_recipe], lambda _, __, ___: True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
                data=ListRecipesResponse(
                    recipes=[
                        ListRecipesItem.model_validate(recipe)
                        for recipe in [example_public_recipe, example_private_with_viewer_recipe]
                    ]
                )
            ).model_dump(mode="json")
        ),
        # Unauthenticated user, should only see public recipes
        (
            (None, UnauthenticatedUser()), [example_public_recipe, example_private_recipe],
            lambda recipe, _, __: not recipe.private, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
                data=ListRecipesResponse(
                    recipes=[
                        ListRecipesItem.model_validate(recipe)
                        for recipe in [example_public_recipe]
                    ]
                )
            ).model_dump(mode="json")
        ),
    ]
)
def test_list(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    mock_get_auth,
    mock_list_recipes,
    mock_authorize_user,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.list.return_value = mock_list_recipes
    mock_recipe_authorize_handler.authorize.side_effect = mock_authorize_user

    response = mock_client.get(f"/{mock_endpoint}/")

    assert response.status_code == expected_status
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "recipe_id,mock_get_auth,mock_get_recipe,mock_authorize_user,expected_status,expected_content",
    [
        # User is authenticated, public recipe, no ACL, should allow
        (
            example_public_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
                data=GetRecipeResponse.model_validate(example_public_recipe)
            ).model_dump(mode="json")
        ),
        # User is authenticated, private recipe, no ACL, should deny
        (
            example_private_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_recipe, False, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.GET.value} recipe with id `{example_private_recipe.display_id}`: "
                       f"`user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is authenticated, public recipe, allow VIEWER user, should allow
        (
            example_public_with_viewer_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_with_viewer_recipe, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
                data=GetRecipeResponse.model_validate(example_public_with_viewer_recipe)
            ).model_dump(mode="json")
        ),
        # User is authenticated, private recipe, allow VIEWER user, should allow
        (
            example_private_with_viewer_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_with_viewer_recipe, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
                data=GetRecipeResponse.model_validate(example_private_with_viewer_recipe)
            ).model_dump(mode="json")
        ),
        # User is authenticated, private recipe, allow UNDEFINED user, should deny
        (
            example_private_with_undefined_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_with_undefined_recipe, False, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.GET.value} recipe with id "
                       f"`{example_private_with_undefined_recipe.display_id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # User is not authenticated, public recipe, allow VIEWER user, should allow
        (
            example_public_with_viewer_recipe.display_id, (None, UnauthenticatedUser()),
            example_public_with_viewer_recipe, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
                data=GetRecipeResponse.model_validate(example_public_with_viewer_recipe)
            ).model_dump(mode="json")
        ),
        # User is not authenticated, private recipe, allow VIEWER user, should deny
        (
            example_private_with_viewer_recipe.display_id, (None, UnauthenticatedUser()),
            example_private_with_viewer_recipe, False, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.GET.value} recipe with id "
                       f"`{example_private_with_viewer_recipe.display_id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Recipe is deleted, should deny
        (
            example_deleted_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_deleted_recipe, True, 404,
            BaseResponse(
                detail=f"Could not {Recipe.Action.GET.value} recipe with id "
                       f"`{example_deleted_recipe.display_id}`: `it does not exist`.",
                data=None
            ).model_dump(mode="json")
        )
    ]
)
def test_get(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    mock_authorize_user,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.get.return_value = mock_get_recipe
    mock_recipe_authorize_handler.authorize.return_value = mock_authorize_user

    response = mock_client.get(f"/{mock_endpoint}/{recipe_id}")

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "mock_get_auth, request_body, mock_authorize_user, expected_status, expected_content",
    [
        # Unauthenticated user
        (
            (None, UnauthenticatedUser()), {"name": "New Recipe"}, True, 401,
            BaseResponse(
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authenticated`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Authenticated, but not authorized
        (
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), {"name": "New Recipe"}, False, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authorized`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Authenticated and authorized
        (
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_admin_user), {"name": "New Recipe"}, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.CREATE.value} finished successfully.",
                data=CreateRecipeResponse(id=example_nonexistent_id)
            ).model_dump(mode="json")
        )
    ]
)
def test_create(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    mock_get_auth,
    request_body,
    mock_authorize_user,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_authorize_handler.authorize.return_value = mock_authorize_user
    mock_recipe_storage_handler.create.return_value = None

    with patch('internal.service.fastapi.resources.recipe.uuid4') as mock_uuid_module:
        mock_uuid_module.return_value = example_nonexistent_id
        request = BaseRequest(data=CreateRecipeRequest.model_validate(request_body))
        response = mock_client.post(f"/{mock_endpoint}/", json=request.model_dump(mode="json"))

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "recipe_id, mock_get_auth, mock_get_recipe, mock_authorize_user, request_body, expected_status, expected_content",
    [
        # Valid update
        (
            example_public_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, True, {"name": "Updated Name"}, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.UPDATE.value} finished successfully.",
                data=UpdateRecipeResponse.model_validate(example_public_recipe)
            ).model_dump(mode="json")
        ),
        # Forbidden
        (
            example_private_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_recipe, False, {}, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.UPDATE.value} recipe with id "
                       f"`{example_private_recipe.display_id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Not found
        (
            str(example_nonexistent_id), (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            None, True, {}, 404,
            BaseResponse(
                detail=f"Could not {Recipe.Action.UPDATE.value} recipe with id "
                       f"`{str(example_nonexistent_id)}`: `it does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Invalid request body
        (
            example_public_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, True, {}, 400,
            BaseResponse(
                detail=f"Could not {Recipe.Action.UPDATE.value} recipe: `all data fields cannot be null`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_update(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    mock_authorize_user,
    request_body,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.get.return_value = mock_get_recipe
    mock_recipe_authorize_handler.authorize.return_value = mock_authorize_user
    mock_recipe_storage_handler.update.return_value = None

    request = BaseRequest(data=UpdateRecipeRequest(**request_body))
    response = mock_client.put(f"/{mock_endpoint}/{recipe_id}", json=request.model_dump(mode="json"))

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "recipe_id, mock_get_auth, mock_get_recipe, mock_authorize_user, expected_status, expected_content",
    [
        # Valid delete
        (
            example_public_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.DELETE.value} finished successfully.",
                data=DeleteRecipeResponse.model_validate(example_public_recipe)
            ).model_dump(mode="json")
        ),
        # Forbidden
        (
            example_private_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_recipe, False, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.DELETE.value} recipe with id "
                       f"`{example_private_recipe.display_id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
        # Not found
        (
            str(example_nonexistent_id), (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user), None, True, 404,
            BaseResponse(
                detail=f"Could not {Recipe.Action.DELETE.value} recipe with id "
                       f"`{str(example_nonexistent_id)}`: `it does not exist`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_delete(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    mock_authorize_user,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.get.return_value = mock_get_recipe
    mock_recipe_authorize_handler.authorize.return_value = mock_authorize_user
    mock_recipe_storage_handler.delete.return_value = None

    response = mock_client.delete(f"/{mock_endpoint}/{recipe_id}")

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "recipe_id, mock_get_auth, mock_get_recipe, mock_authorize_user, expected_status, expected_content",
    [
        # Authorized user
        (
            example_public_recipe.display_id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, True, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET_METADATA.value} finished successfully.",
                data=GetMetadataResponse.model_validate(example_public_recipe)
            ).model_dump(mode="json")
        ),
        # Forbidden
        (
            example_private_recipe.display_id,
            (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_recipe, False, 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.GET_METADATA.value} recipe with id "
                       f"`{example_private_recipe.display_id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_get_metadata(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    mock_authorize_user,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.get.return_value = mock_get_recipe
    mock_recipe_authorize_handler.authorize.return_value = mock_authorize_user

    response = mock_client.get(f"/{mock_endpoint}/{recipe_id}/metadata")

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content


@pytest.mark.parametrize(
    "recipe_id, mock_get_auth, mock_get_recipe, mock_authorize_user, mock_messages, expected_status, expected_content",
    [
        # Authorized user
        (
            example_public_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_public_recipe, True, example_messages, 200,
            BaseResponse(
                detail=f"Recipe {Recipe.Action.GET_MESSAGES.value} finished successfully.",
                data=GetMessagesResponse(
                    messages=[GetMessagesItem.model_validate(message) for message in example_messages]
                )
            ).model_dump(mode="json")
        ),
        # Forbidden
        (
            example_private_recipe.display_id, (AuthCredentials([SERVICE_AUTH_SCOPE]), example_user),
            example_private_recipe, False, [], 403,
            BaseResponse(
                detail=f"Could not {Recipe.Action.GET_MESSAGES.value} recipe with id "
                       f"`{example_private_recipe.display_id}`: `user is forbidden`.",
                data=None
            ).model_dump(mode="json")
        ),
    ]
)
def test_get_messages(
    mock_authenticate_backend,
    mock_client,
    mock_recipe_storage_handler,
    mock_recipe_agent_handler,
    mock_recipe_authorize_handler,
    mock_endpoint,
    recipe_id,
    mock_get_auth,
    mock_get_recipe,
    mock_authorize_user,
    mock_messages,
    expected_status,
    expected_content,
):
    mock_authenticate_backend.authenticate.side_effect = awaitable_return(mock_get_auth)
    mock_recipe_storage_handler.get.return_value = mock_get_recipe
    mock_recipe_authorize_handler.authorize.return_value = mock_authorize_user

    async def message_generator(*args, **kwargs):
        for msg in mock_messages:
            yield msg

    mock_recipe_agent_handler.get_messages = message_generator
    response = mock_client.get(f"/{mock_endpoint}/{recipe_id}/message")

    assert response.status_code == expected_status
    if expected_content["data"] is None:
        del expected_content["data"]
    assert response.json() == expected_content

    if expected_status == 200:
        assert len(response.json()["data"]["messages"]) == len(mock_messages)

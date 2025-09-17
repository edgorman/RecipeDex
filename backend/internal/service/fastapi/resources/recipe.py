from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, WebSocket, WebSocketException, WebSocketDisconnect, HTTPException, status, Query
from starlette.authentication import BaseUser

from internal.agent.recipe import RecipeAgent
from internal.auth.recipe import RecipeAuthorize
from internal.objects.user import User
from internal.objects.recipe import Recipe
from internal.objects.session import Session
from internal.storage.recipe import RecipeStorage
from internal.service.fastapi.middleware.authenticate import get_user_from_request
from internal.service.fastapi.schemas import BaseRequest, BaseResponse
from internal.service.fastapi.schemas.recipe import (
    ListRecipesResponse, ListRecipesItem, GetRecipeResponse, GetMetadataResponse, GetMessagesResponse, GetMessagesItem,
    CreateRecipeRequest, CreateRecipeResponse, UpdateRecipeRequest, UpdateRecipeResponse, DeleteRecipeResponse,
    SendMessageRequest, SendMessageResponse
)


class RecipeResource(APIRouter):
    """The RecipeResource is the API resource for recipes."""

    def __init__(
            self,
            recipe_storage_handler: RecipeStorage,
            recipe_agent_handler: RecipeAgent,
            recipe_authorize_handler: RecipeAuthorize,
            endpoint="recipe"
    ):
        """
        Initialise the RecipeResource.

        Args:
            recipe_storage_handler: the handler for recipe storage.
            recipe_agent_handler: the handler for the recipe agent.
            recipe_authorize_handler: the handler for recipe authorization.
            endpoint: the endpoint to mount the resource on.
        """
        super().__init__(prefix=f"/{endpoint}")
        self.__recipe_storage_handler = recipe_storage_handler
        self.__recipe_agent_handler = recipe_agent_handler
        self.__recipe_authorize_handler = recipe_authorize_handler

        # Add the API routes for the resource.
        self.add_api_route(
            "/",
            self._list,
            methods=["GET"],
            response_model=BaseResponse[ListRecipesResponse]
        )
        self.add_api_route(
            "/{recipe_id}",
            self._get,
            methods=["GET"],
            response_model=BaseResponse[GetRecipeResponse]
        )
        self.add_api_route(
            "/{recipe_id}/metadata",
            self._get_metadata,
            methods=["GET"],
            response_model=BaseResponse[GetMetadataResponse]
        )
        self.add_api_route(
            "/{recipe_id}/message",
            self._get_messages,
            methods=["GET"],
            response_model=BaseResponse[GetMessagesResponse]
        )
        self.add_api_route(
            "/",
            self._create,
            methods=["POST"],
            response_model=BaseResponse[CreateRecipeResponse]
        )
        self.add_api_route(
            "/{recipe_id}",
            self._update,
            methods=["PUT"],
            response_model=BaseResponse[UpdateRecipeResponse]
        )
        self.add_api_route(
            "/{recipe_id}",
            self._delete,
            methods=["DELETE"],
            response_model=BaseResponse[DeleteRecipeResponse]
        )
        self.add_api_websocket_route(
            "/{recipe_id}/message",
            self._message,
            "message"
        )

    def __preprocess(self, recipe_id: str, request_user: User, request_action: Recipe.Action) -> Recipe:
        """
        Preprocess a request by validating the recipe ID, checking for existence, and authorizing the user.

        Args:
            recipe_id: the ID of the recipe to preprocess.
            request_user: the user making the request.
            request_action: the action being performed.

        Returns:
            the recipe if it exists and the user is authorized.

        Raises:
            HTTPException: if the recipe ID is invalid, the recipe does not exist, or the user is not authorized.
        """
        try:
            # Validate the recipe ID.
            recipe_id = UUID(recipe_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {request_action.value} recipe with id `{recipe_id}`: `invalid recipe id, {str(e)}`."
            )

        # Get the recipe from storage.
        recipe = self.__recipe_storage_handler.get(recipe_id)
        if recipe is None or recipe.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {request_action.value} recipe with id `{str(recipe_id)}`: `it does not exist`."
            )

        # Authorize the user for the action.
        authorized = self.__recipe_authorize_handler.authorize(recipe, request_action, request_user)
        if not authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {request_action.value} recipe with id `{str(recipe_id)}`: `user is forbidden`."
            )

        return recipe

    async def _list(
        self,
        request_user: BaseUser = Depends(get_user_from_request),
        page: int = Query(0, ge=0),
        page_size: int = Query(25, ge=1, le=100),
    ) -> BaseResponse[ListRecipesResponse]:
        """
        List recipes.

        Args:
            request_user: the user making the request.
            page: the page number to return.
            page_size: the number of items to return per page.

        Returns:
            a list of recipes.
        """
        try:
            # List recipes from storage.
            recipes = self.__recipe_storage_handler.list(page=page, page_size=page_size)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {Recipe.Action.GET.value} recipes: `{str(e)}`."
            )

        # Filter out recipes that the user is not authorized to see.
        recipes = [
            recipe
            for recipe in recipes if self.__recipe_authorize_handler.authorize(recipe, Recipe.Action.GET, request_user)
        ]

        try:
            # Format the response.
            data = ListRecipesResponse(recipes=[ListRecipesItem.model_validate(recipe) for recipe in recipes])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.GET.value} finished successfully.", data=data)

    async def _get(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetRecipeResponse]:
        """
        Get a recipe by ID.

        Args:
            recipe_id: the ID of the recipe to get.
            request_user: the user making the request.

        Returns:
            the recipe.
        """
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.GET)

        try:
            # Format the response.
            data = GetRecipeResponse.model_validate(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.GET.value} finished successfully.", data=data)

    async def _get_metadata(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetMetadataResponse]:
        """
        Get the metadata for a recipe.

        Args:
            recipe_id: the ID of the recipe to get metadata for.
            request_user: the user making the request.

        Returns:
            the recipe metadata.
        """
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.GET_METADATA)

        try:
            # Format the response.
            data = GetMetadataResponse.model_validate(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.GET_METADATA.value} finished successfully.", data=data)

    async def _get_messages(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetMessagesResponse]:
        """
        Get the messages for a recipe.

        Args:
            recipe_id: the ID of the recipe to get messages for.
            request_user: the user making the request.

        Returns:
            the recipe messages.
        """
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.GET_MESSAGES)
        messages = [m async for m in self.__recipe_agent_handler.get_messages(recipe, request_user)]

        try:
            # Format the response.
            data = GetMessagesResponse(messages=[GetMessagesItem.model_validate(message) for message in messages])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.GET_MESSAGES.value} finished successfully.", data=data)

    async def _create(
        self,
        request: BaseRequest[CreateRecipeRequest],
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[CreateRecipeResponse]:
        """
        Create a new recipe.

        Args:
            request: the request to create the recipe.
            request_user: the user making the request.

        Returns:
            the created recipe.
        """
        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authenticated`."
            )
        authenticated_user: User = request_user

        try:
            # Create the recipe object from the request data.
            data = request.data.model_dump()
            recipe_args = {"id": uuid4(), "user_role_mapping": {authenticated_user.id: Recipe.Role.OWNER}} | data
            recipe = Recipe(**recipe_args)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `{str(e)}`."
            )

        # Authorize the user for the action.
        is_authorized = self.__recipe_authorize_handler.authorize(recipe, Recipe.Action.CREATE, authenticated_user)
        if not is_authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authorized`."
            )

        try:
            # Create the recipe in storage.
            self.__recipe_storage_handler.create(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `{e}`."
            )

        try:
            # Format the response.
            data = CreateRecipeResponse.model_validate(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.CREATE.value} finished successfully.", data=data)

    async def _update(
        self,
        request: BaseRequest[UpdateRecipeRequest],
        recipe_id: str,
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[UpdateRecipeResponse]:
        """
        Update a recipe.

        Args:
            request: the request to update the recipe.
            recipe_id: the ID of the recipe to update.
            request_user: the user making the request.

        Returns:
            the updated recipe.
        """
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.UPDATE)

        try:
            # Update the recipe object from the request data.
            data = request.data.model_dump()

            if all([field is None for field in data.values()]):
                raise ValueError("all data fields cannot be null")

            for field, value in data.items():
                if value is None:
                    continue

                try:
                    setattr(recipe, field, value)
                except Exception as e:
                    raise ValueError(f"bad value for Recipe.{field}, `{value}`: {str(e)}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {Recipe.Action.UPDATE.value} recipe: `{e}`."
            )

        try:
            # Update the recipe in storage.
            self.__recipe_storage_handler.update(recipe.id, recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {Recipe.Action.UPDATE.value} recipe: `{e}`."
            )

        try:
            # Format the response.
            data = UpdateRecipeResponse.model_validate(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.UPDATE.value} finished successfully.", data=data)

    async def _delete(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[DeleteRecipeResponse]:
        """
        Delete a recipe.

        Args:
            recipe_id: the ID of the recipe to delete.
            request_user: the user making the request.

        Returns:
            the deleted recipe.
        """
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.DELETE)

        # Delete the recipe from storage.
        self.__recipe_storage_handler.delete(recipe.id)

        try:
            # Format the response.
            data = DeleteRecipeResponse.model_validate(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"Recipe {Recipe.Action.DELETE.value} finished successfully.", data=data)

    async def _message(self, connection: WebSocket, recipe_id: str) -> None:
        """
        Send a message to a recipe.

        Args:
            connection: the WebSocket connection.
            recipe_id: the ID of the recipe to send the message to.
        """
        request_user: User = get_user_from_request(connection)
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.MESSAGE)

        try:
            await connection.accept()

            while True:
                # Receive a message from the client.
                data = await connection.receive_json()

                try:
                    # Validate the request data.
                    request_data = SendMessageRequest.model_validate(data)
                    request_message = Session.Message(
                        role=Session.Message.Role.USER,
                        value=request_data.value
                    )
                except Exception as e:
                    await connection.send_json(
                        BaseResponse(
                            detail=f"Could not {Recipe.Action.GET_MESSAGES.value} Recipe, "
                                   f"invalid request data: {str(e)}.",
                            data=None
                        ).model_dump(mode="json")
                    )

                try:
                    # Send a confirmation to the client.
                    await connection.send_json(
                        BaseResponse(
                            detail=f"Recipe {Recipe.Action.GET_MESSAGES.value} received data successfully.",
                            data=None
                        ).model_dump(mode="json")
                    )

                    # Create a message with the recipe agent and stream the response.
                    async for response_message in self.__recipe_agent_handler.create_message(
                        recipe, request_user, request_message
                    ):
                        await connection.send_json(
                            BaseResponse(
                                detail=f"Recipe {Recipe.Action.GET_MESSAGES.value} responded successfully.",
                                data=SendMessageResponse.model_validate(response_message)
                            ).model_dump(mode="json")
                        )
                except Exception as e:
                    await connection.send_json(
                        BaseResponse(
                            detail=f"Could not {Recipe.Action.GET_MESSAGES.value} Recipe, "
                                   f"experienced internal error: {str(e)}.",
                            data=None
                        ).model_dump(mode="json")
                    )

        except WebSocketException as we:
            # Handle WebSocket errors.
            await connection.send_json(
                BaseResponse(
                    detail=f"Could not {Recipe.Action.GET_MESSAGES.value} Recipe, "
                           f"experienced websocket error: `{str(we.reason)}`.",
                    data=None
                ).model_dump(mode="json")
            )
        except WebSocketDisconnect:
            # Handle client disconnects.
            pass

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, WebSocket, WebSocketException, WebSocketDisconnect, HTTPException, status, Query
from starlette.authentication import BaseUser

from internal.agent.recipe import RecipeAgent
from internal.auth.recipe import RecipeAuthorize
from internal.objects.user import User
from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage
from internal.service.fastapi.resources import BaseRequest, BaseResponse
from internal.service.fastapi.middleware.authenticate import get_user_from_request


class RecipeResource(APIRouter):
    def __init__(
            self,
            recipe_storage_handler: RecipeStorage,
            recipe_agent_handler: RecipeAgent,
            recipe_authorize_handler: RecipeAuthorize,
            endpoint="recipe"
    ):
        super().__init__(prefix=f"/{endpoint}")
        self.__recipe_storage_handler = recipe_storage_handler
        self.__recipe_agent_handler = recipe_agent_handler
        self.__recipe_authorize_handler = recipe_authorize_handler

        self.add_api_route("/", self._list, methods=["GET"])
        self.add_api_route("/{recipe_id}", self._get, methods=["GET"])
        self.add_api_route("/{recipe_id}/metadata", self._get_metadata, methods=["GET"])
        self.add_api_route("/", self._create, methods=["POST"])
        self.add_api_route("/{recipe_id}", self._update, methods=["PUT"])
        self.add_api_route("/{recipe_id}", self._delete, methods=["DELETE"])
        self.add_api_route("/{recipe_id}/message", self._get_messages, methods=["GET"])
        self.add_api_websocket_route("/{recipe_id}/message", self._message, "message")

    def __preprocess(self, recipe_id: str, request_user: User, request_action: Recipe.Action) -> Recipe:
        try:
            recipe_id = UUID(recipe_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {request_action.value} recipe with id `{recipe_id}`: `invalid recipe id, {str(e)}`."
            )

        recipe = self.__recipe_storage_handler.get(recipe_id)
        if recipe is None or recipe.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {request_action.value} recipe with id `{str(recipe_id)}`: `it does not exist`."
            )

        authorized = self.__recipe_authorize_handler.authorize(recipe, request_action, request_user)
        if not authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {request_action.value} recipe with id `{str(recipe_id)}`: `user is forbidden`."
            )

        return recipe

    @dataclass
    class ListRecipesItem:
        id: str
        name: str
        private: bool

    @dataclass
    class ListRecipesResponse:
        recipes: List["RecipeResource.ListRecipesItem"]

    async def _list(
        self,
        request_user: BaseUser = Depends(get_user_from_request),
        page: int = Query(0, ge=0),
        page_size: int = Query(25, ge=1, le=100),
    ) -> BaseResponse[ListRecipesResponse]:
        try:
            recipes = self.__recipe_storage_handler.list(page=page, page_size=page_size)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not list recipes: `{str(e)}`."
            )

        authorized_recipes = [
            self.ListRecipesItem(id=recipe.display_id, name=recipe.display_name, private=recipe.private)
            for recipe in recipes if self.__recipe_authorize_handler.authorize(recipe, Recipe.Action.GET, request_user)
        ]

        return BaseResponse(
            detail="Recipe list finished successfully.",
            data=self.ListRecipesResponse(recipes=authorized_recipes)
        )

    @dataclass
    class GetRecipeResponse:
        id: str
        name: str
        ingredients: List[Recipe.Ingredient]
        instructions: List[Recipe.Instruction]

    async def _get(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetRecipeResponse]:
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.GET)

        return BaseResponse(
            detail=f"Recipe {Recipe.Action.GET.value} finished successfully.",
            data=self.GetRecipeResponse(
                id=recipe.display_id,
                name=recipe.display_name,
                ingredients=recipe.ingredients,
                instructions=recipe.instructions
            )
        )

    @dataclass
    class GetMetadataResponse:
        id: str
        session_id: Optional[str]
        deleted: bool
        private: bool
        user_role_mapping: Dict[UUID, Recipe.Role]

    async def _get_metadata(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetMetadataResponse]:
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.METADATA)

        return BaseResponse(
            detail=f"Recipe {Recipe.Action.METADATA.value} finished successfully.",
            data=self.GetMetadataResponse(
                id=recipe.display_id,
                session_id=recipe.session_id,
                deleted=recipe.deleted,
                private=recipe.private,
                user_role_mapping=recipe.user_role_mapping
            )
        )

    @dataclass
    class CreateRecipeRequest:
        name: Optional[str] = "Untitled Recipe"
        private: Optional[bool] = False

    @dataclass
    class CreateRecipeResponse:
        id: str

    async def _create(
        self,
        request: BaseRequest[CreateRecipeRequest],
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[CreateRecipeResponse]:
        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authenticated`."
            )

        recipe = Recipe(
            id=uuid4(),
            name=request.data.name,
            private=request.data.private,
            user_role_mapping={request_user.id: Recipe.Role.OWNER}
        )

        authorized = self.__recipe_authorize_handler.authorize(recipe, Recipe.Action.CREATE, request_user)
        if not authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authorized`."
            )

        try:
            self.__recipe_storage_handler.create(recipe)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `{e}`."
            )

        return BaseResponse(
            detail=f"Recipe {Recipe.Action.CREATE.value} finished successfully.",
            data=self.CreateRecipeResponse(id=recipe.display_id)
        )

    @dataclass
    class UpdateRecipeRequest:
        name: Optional[str] = None
        deleted: Optional[bool] = None
        private: Optional[bool] = None
        user_role_mapping: Optional[Dict[UUID, Recipe.Role]] = field(default_factory=dict)
        ingredients: List[Recipe.Ingredient] = field(default_factory=list)
        instructions: List[Recipe.Instruction] = field(default_factory=list)

    @dataclass
    class UpdateRecipeResponse:
        id: str

    async def _update(
        self,
        request: BaseRequest[UpdateRecipeRequest],
        recipe_id: str,
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[UpdateRecipeResponse]:
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.UPDATE)

        # TODO: parse request params to their appropriate types
        self.__recipe_storage_handler.update(recipe.id, **asdict(request))

        return BaseResponse(
            detail=f"Recipe {Recipe.Action.UPDATE.value} finished successfully.",
            data=self.UpdateRecipeResponse(id=recipe.display_id)
        )

    @dataclass
    class DeleteRecipeResponse:
        id: str

    async def _delete(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[DeleteRecipeResponse]:
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.DELETE)

        self.__recipe_storage_handler.delete(recipe.id)

        return BaseResponse(
            detail=f"Recipe {Recipe.Action.DELETE.value} finished successfully.",
            data=self.DeleteRecipeResponse(id=recipe.display_id)
        )

    @dataclass
    class GetMessagesResponse:
        messages: List[Recipe.Message] = field(default_factory=list)

    async def _get_messages(
        self, recipe_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetMessagesResponse]:
        recipe = self.__preprocess(recipe_id, request_user, Recipe.Action.MESSAGE)
        messages = [m async for m in self.__recipe_agent_handler.get_messages(recipe)]

        return BaseResponse(
            detail=f"Recipe {Recipe.Action.MESSAGE.value} finished successfully.",
            data=self.GetMessagesResponse(messages=messages)
        )

    async def _message(self, connection: WebSocket, recipe_id: str):
        user: User = connection.user
        recipe = self.__preprocess(recipe_id, user, Recipe.Action.MESSAGE)

        try:
            await connection.accept()

            while True:
                data = await connection.receive_json()

                if "message" not in data:
                    await connection.send_json(
                        {
                            "detail": f"Could not {Recipe.Action.MESSAGE.value} Recipe, missing `message` field.",
                            "data": None
                        }
                    )

                try:
                    await connection.send_json(
                        {
                            "detail": f"Recipe {Recipe.Action.MESSAGE.value} received data successfully.",
                            "data": None
                        }
                    )

                    message = Recipe.Message(user.display_id, Recipe.Message.Role.USER, data.get("message"))
                    async for response in self.__recipe_agent_handler.create_message(recipe, message):
                        await connection.send_json(
                            {
                                "detail": f"Recipe {Recipe.Action.MESSAGE.value} responded successfully.",
                                "data": response
                            }
                        )
                except Exception as e:
                    await connection.send_json(
                        {
                            "detail": f"Could not {Recipe.Action.MESSAGE.value} Recipe, "
                                      f"experienced internal error: {str(e)}.",
                            "data": None
                        }
                    )

        except WebSocketException as we:
            await connection.send_json(
                {
                    "detail": f"Could not {Recipe.Action.MESSAGE.value} Recipe, "
                              f"experienced websocket error: `{str(we.reason)}`.",
                    "data": None
                }
            )
        except WebSocketDisconnect:
            pass

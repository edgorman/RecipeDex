from uuid import uuid4, UUID
from fastapi import APIRouter, Request, WebSocket, WebSocketException, WebSocketDisconnect, HTTPException, status
from fastapi.responses import JSONResponse

from internal.agent.recipe import RecipeAgent
from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage
from internal.objects.user import User


class RecipeResource(APIRouter):
    def __init__(self, recipe_storage_handler: RecipeStorage, recipe_agent_handler: RecipeAgent, endpoint="recipe"):
        super().__init__(prefix=f"/{endpoint}")
        self.__recipe_storage_handler = recipe_storage_handler
        self.__recipe_agent_handler = recipe_agent_handler

        self.add_api_route("/{recipe_id}", self._get, methods=["GET"])
        self.add_api_route("/{recipe_id}/metadata", self._get_metadata, methods=["GET"])
        self.add_api_route("/{recipe_id}", self._create, methods=["POST"])
        self.add_api_route("/{recipe_id}", self._update, methods=["PUT"])
        self.add_api_route("/{recipe_id}", self._delete, methods=["DELETE"])
        self.add_api_route("/{recipe_id}/message", self._message, methods=["POST"])
        self.add_api_websocket_route("/{recipe_id}/message", self._message)

    def __preprocess(self, recipe_id: str, user: User, action: Recipe.Action) -> Recipe:
        try:
            recipe_id = UUID(recipe_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not {action.value} recipe with id `{recipe_id}`: `invalid recipe id, {str(e)}`."
            )

        recipe = self.__recipe_storage_handler.get(recipe_id)
        if recipe is None or recipe.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {action.value} recipe with id `{str(recipe_id)}`: `it does not exist`."
            )

        user_id = user.id if user.is_authenticated else None
        if not recipe.authorize(user_id, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {action.value} recipe with id `{str(recipe_id)}`: `user is not authorized`."
            )

        return recipe

    async def _get(self, connection: Request, recipe_id: str):
        user: User = connection.user
        recipe = self.__preprocess(recipe_id, user, Recipe.Action.GET)

        return JSONResponse(
            {
                "recipe": {
                    "id": str(recipe.id),
                },
                "detail": f"Recipe {Recipe.Action.GET.value} finished successfully."
            }
        )

    async def _get_metadata(self, connection: Request, recipe_id: str):
        user: User = connection.user
        recipe = self.__preprocess(recipe_id, user, Recipe.Action.METADATA)

        return JSONResponse(
            {
                "recipe": recipe.to_dict(),
                "detail": f"Recipe {Recipe.Action.METADATA.value} finished successfully."
            }
        )

    async def _create(self, connection: Request):
        user: User = connection.user
        if not user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authenticated`."
            )

        # TODO: update roles that can create recipes beyond admin role
        if user.role != User.Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {Recipe.Action.CREATE.value} recipe: `user is not authorized`."
            )

        # TODO: parse recipe from connection body params
        recipe = Recipe(
            id=uuid4(),
            private=False,
            user_access_mapping={user.id: Recipe.Role.OWNER}
        )
        self.__recipe_storage_handler.create(recipe)

        return JSONResponse(
            {
                "recipe_id": str(recipe.id),
                "detail": f"Recipe {Recipe.Action.CREATE.value} finished successfully."
            }
        )

    async def _update(self, connection: Request, recipe_id: str):
        user: User = connection.user
        recipe = self.__preprocess(recipe_id, user, Recipe.Action.UPDATE)

        # TODO: parse recipe from connection body params
        self.__recipe_storage_handler.update(recipe.id, None)

        return JSONResponse(
            {
                "recipe_id": str(recipe.id),
                "detail": f"Recipe {Recipe.Action.UPDATE.value} finished successfully."
            }
        )

    async def _delete(self, connection: Request, recipe_id: str):
        user: User = connection.user
        recipe = self.__preprocess(recipe_id, user, Recipe.Action.DELETE)

        self.__recipe_storage_handler.delete(recipe.id)

        return JSONResponse(
            {
                "recipe_id": recipe_id,
                "detail": f"Recipe {Recipe.Action.DELETE.value} finished successfully."
            }
        )

    async def _message(self, connection: WebSocket, recipe_id: str):
        user: User = connection.user
        recipe = self.__preprocess(recipe_id, user, Recipe.Action.MESSAGE)

        try:
            await connection.accept()

            while True:
                data = await connection.receive_json()
                message = data.get("message")

                if not message:
                    await connection.send_json(
                        {
                            "response": None,
                            "detail": f"Could not {Recipe.Action.MESSAGE.value} Recipe, missing `message` field."
                        }
                    )

                try:
                    await connection.send_json(
                        {
                            "response": None,
                            "detail": f"Recipe {Recipe.Action.MESSAGE.value} received message successfully."
                        }
                    )

                    async for response in self.__recipe_agent_handler.message(user, recipe, message):
                        await connection.send_json(
                            {
                                "response": response,
                                "detail": f"Recipe {Recipe.Action.MESSAGE.value} responded successfully."
                            }
                        )
                except Exception as e:
                    await connection.send_json(
                        {
                            "response": None,
                            "detail": f"Could not {Recipe.Action.MESSAGE.value} Recipe, "
                                      f"experienced internal error: {str(e)}."
                        }
                    )

        except WebSocketException as we:
            await connection.send_json(
                {
                    "response": None,
                    "detail": f"Could not {Recipe.Action.MESSAGE.value} Recipe, "
                              f"experienced websocket error: `{str(we.reason)}`."
                }
            )
        except WebSocketDisconnect:
            pass

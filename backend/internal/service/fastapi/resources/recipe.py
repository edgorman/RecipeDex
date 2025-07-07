from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from internal.agents.recipe import RecipeAgent
from internal.objects.recipe import Recipe, RecipeAction
from internal.storage.recipe import RecipeStorage
from internal.objects.user import User


class RecipeResource(APIRouter):
    def __init__(self, recipe_storage_handler: RecipeStorage, recipe_agent_handler: RecipeAgent, endpoint="recipe"):
        super().__init__(prefix=f"/{endpoint}")
        self.__recipe_storage_handler = recipe_storage_handler
        self.__recipe_agent_handler = recipe_agent_handler

        self.add_api_route("/{recipe_id}", self._get, methods=["GET"])
        self.add_api_route("/{recipe_id}", self._create, methods=["POST"])
        self.add_api_route("/{recipe_id}", self._update, methods=["PUT"])
        self.add_api_route("/{recipe_id}", self._delete, methods=["DELETE"])
        self.add_api_route("/{recipe_id}/message", self._message, methods=["POST"])

    def __preprocess(self, recipe_id: str, user: User, action: RecipeAction) -> Recipe:
        recipe = self.__recipe_storage_handler.get(recipe_id)
        if recipe is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not {action.value} recipe with id `{recipe_id}`: `it does not exist`."
            )

        user_id = user.id if user.is_authenticated else None
        if not recipe.authorize(user_id, action):
            raise HTTPException(
                status_code=403,
                detail=f"Could not {action.value} recipe with id `{recipe_id}`: `user is not authorized`."
            )

        return recipe

    async def _get(self, request: Request, recipe_id: str):
        recipe = self.__preprocess(recipe_id, request.user, RecipeAction.GET)
        return JSONResponse(
            {
                "recipe": recipe.to_dict(),
                "detail": f"Recipe {RecipeAction.GET.value} finished successfully."
            }
        )

    async def _create(self, request: Request):
        user: User = request.user
        if not user.is_authenticated:
            raise HTTPException(
                status_code=401,
                detail=f"Could not {RecipeAction.CREATE.value} recipe: `user is not authenticated`."
            )

        # TODO: parse recipe from request body params
        recipe_id = self.__recipe_storage_handler.create()

        return JSONResponse(
            {
                "recipe_id": recipe_id,
                "detail": f"Recipe {RecipeAction.CREATE.value} finished successfully."
            }
        )

    async def _update(self, request: Request, recipe_id: str):
        _ = self.__preprocess(recipe_id, request.user, RecipeAction.UPDATE)

        # TODO: parse recipe from request body params
        self.__recipe_storage_handler.update()

        return JSONResponse(
            {
                "recipe_id": recipe_id,
                "detail": f"Recipe {RecipeAction.UPDATE.value} finished successfully."
            }
        )

    async def _delete(self, request: Request, recipe_id: str):
        _ = self.__preprocess(recipe_id, request.user, RecipeAction.DELETE)

        self.__recipe_storage_handler.update()

        return JSONResponse(
            {
                "recipe_id": recipe_id,
                "detail": f"Recipe {RecipeAction.DELETE.value} finished successfully."
            }
        )

    async def _message(self, request: Request, recipe_id: str):
        recipe = self.__preprocess(recipe_id, request.user, RecipeAction.UPDATE)

        try:
            self.__recipe_storage_handler.update()  # TODO: update chat
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not {RecipeAction.UPDATE.value} recipe: `{str(e)}`."
            )

        try:
            _ = self.__recipe_agent_handler.message(request.user, recipe.session, request.body.message)
            self.__recipe_storage_handler.update()  # TODO: update chat
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not {RecipeAction.UPDATE.value} recipe: `{str(e)}`."
            )

        return recipe

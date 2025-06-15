from fastapi import FastAPI, Request
from starlette.authentication import UnauthenticatedUser
import uvicorn

from internal.config.service import (
    NAME as SERVICE_NAME,
    VERSION as SERVICE_VERSION,
    ALLOWED_ORIGIN as SERVICE_ALLOWED_ORIGIN
)
from internal.agents.recipe import RecipeAgent
from internal.service.api import APIService
from internal.storage.user import UserStorage
from internal.storage.recipe import RecipeStorage
from internal.service.fastapi.middleware.cors import add_cors_middleware
from internal.service.fastapi.middleware.authenticate import add_authenticate_middleware


class FastapiAPIService(APIService):

    def __init__(
        self,
        host: str,
        port: int,
        recipe_agent_handler: RecipeAgent,
        recipe_storage_handler: RecipeStorage,
        user_storage_handler: UserStorage,
    ):
        self.__recipe_agent_handler = recipe_agent_handler
        self.__recipe_storage_handler = recipe_storage_handler
        self.__user_storage_handler = user_storage_handler

        self.__api = FastAPI()
        add_authenticate_middleware(self.__api, self.__user_storage_handler)
        add_cors_middleware(self.__api, SERVICE_ALLOWED_ORIGIN)

        self.__api.add_api_route("/", self._root)

        self.__config = uvicorn.Config(self.__api, host=host, port=port, workers=1)
        self.__server = uvicorn.Server(self.__config)

    def run(self):
        self.__server.run()

    async def _root(self, request: Request):
        message = "Hello World :)"
        if not isinstance(request.user, UnauthenticatedUser):
            message = f"Welcome back {request.user.display_name}"

        return {
            "name": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "message": message
        }

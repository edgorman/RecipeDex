from fastapi import FastAPI, Request
from typing import List
import uvicorn

from internal.agent.recipe import RecipeAgent
from internal.objects.user import User
from internal.service.api import APIService
from internal.storage.user import UserStorage
from internal.storage.recipe import RecipeStorage
from internal.service.fastapi.middleware.cors import add_cors_middleware
from internal.service.fastapi.middleware.authenticate import add_authenticate_middleware
from internal.service.fastapi.resources.user import UserResource
from internal.service.fastapi.resources.recipe import RecipeResource


class FastapiAPIService(APIService):
    """The FastAPIService is an implementation of the APIService"""

    def __init__(
        self,
        name: str,
        version: str,
        host: str,
        port: int,
        allowed_origins: List[str],
        recipe_agent_handler: RecipeAgent,
        recipe_storage_handler: RecipeStorage,
        user_storage_handler: UserStorage,
    ):
        self.__name = name
        self.__version = version
        self.__recipe_agent_handler = recipe_agent_handler
        self.__recipe_storage_handler = recipe_storage_handler
        self.__user_storage_handler = user_storage_handler

        self.__api = FastAPI()
        add_authenticate_middleware(self.__api, self.__user_storage_handler)
        add_cors_middleware(self.__api, allowed_origins)

        self.__api.add_api_route("/", self._root)
        self.__api.include_router(UserResource(self.__user_storage_handler))
        self.__api.include_router(RecipeResource(self.__recipe_storage_handler, self.__recipe_agent_handler))

        self.__config = uvicorn.Config(self.__api, host=host, port=port, workers=1)
        self.__server = uvicorn.Server(self.__config)

    def run(self):
        self.__server.run()

    async def _root(self, request: Request):
        message = "Hello World :)"

        user: User = request.user
        if user.is_authenticated:
            message = f"Welcome back {user.display_name}"

        return {
            "name": self.__name,
            "version": self.__version,
            "message": message
        }

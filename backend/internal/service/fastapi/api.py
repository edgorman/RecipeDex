import logging
import uvicorn
from typing import List
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from internal.config.telemetry import TELEMETRY_UVICORN_CONFIG
from internal.agent.recipe import RecipeAgent
from internal.auth.recipe import RecipeAuthorize
from internal.auth.user import UserAuthenticate, UserAuthorize
from internal.service.api import APIService
from internal.storage.user import UserStorage
from internal.storage.recipe import RecipeStorage
from internal.service.fastapi._middleware.cors import add_cors_middleware
from internal.service.fastapi._middleware.auth import add_authenticate_middleware
from internal.service.fastapi._middleware.rate import add_rate_limiter_middleware
from internal.service.fastapi._resources.root import RootResource
from internal.service.fastapi._resources.user import UserResource
from internal.service.fastapi._resources.recipe import RecipeResource


logger = logging.getLogger(__name__)


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
        recipe_authorize_handler: RecipeAuthorize,
        user_storage_handler: UserStorage,
        user_authenticate_handler: UserAuthenticate,
        user_authorize_handler: UserAuthorize
    ):
        """
        Initialise the FastAPIService.

        Args:
            name: the name of the API.
            version: the version of the API.
            host: the host to run the API on.
            port: the port to run the API on.
            allowed_origins: a list of allowed origins for CORS.
            recipe_agent_handler: the handler for the recipe agent.
            recipe_storage_handler: the handler for recipe storage.
            recipe_authorize_handler: the handler for recipe authorization.
            user_storage_handler: the handler for user storage.
            user_authenticate_handler: the handler for user authentication.
            user_authorize_handler: the handler for user authorization.
        """
        self.__name = name
        self.__version = version
        self.__recipe_agent_handler = recipe_agent_handler
        self.__recipe_storage_handler = recipe_storage_handler
        self.__recipe_authorize_handler = recipe_authorize_handler
        self.__user_storage_handler = user_storage_handler
        self.__user_authenticate_handler = user_authenticate_handler
        self.__user_authorize_handler = user_authorize_handler

        # Initialise the FastAPI app and add middleware.
        self.__api = FastAPI()
        FastAPIInstrumentor.instrument_app(self.__api)
        add_authenticate_middleware(self.__api, self.__user_storage_handler, self.__user_authenticate_handler)
        add_cors_middleware(self.__api, allowed_origins)
        add_rate_limiter_middleware(self.__api)

        # Add the API resources.
        self.__api.include_router(
            RootResource(
                name=self.__name,
                version=self.__version
            )
        )
        self.__api.include_router(
            UserResource(
                self.__user_storage_handler,
                self.__user_authorize_handler
            )
        )
        self.__api.include_router(
            RecipeResource(
                self.__recipe_storage_handler,
                self.__recipe_agent_handler,
                self.__recipe_authorize_handler
            )
        )

        # Configure and initialise the uvicorn server.
        self.__config = uvicorn.Config(self.__api, host=host, port=port, log_config=TELEMETRY_UVICORN_CONFIG)
        self.__server = uvicorn.Server(self.__config)
        logger.info("Initialised fastapi service")

    def run(self):
        """Run the API service."""
        logger.info("Running fastapi service...")
        self.__server.run()

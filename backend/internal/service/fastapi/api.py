import logging
import uvicorn
from typing import List
from starlette.authentication import BaseUser
from fastapi import FastAPI, Depends, HTTPException, status
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from internal.config.telemetry import TELEMETRY_UVICORN_CONFIG
from internal.agent.recipe import RecipeAgent
from internal.auth.recipe import RecipeAuthorize
from internal.auth.user import UserAuthenticate, UserAuthorize
from internal.service.api import APIService
from internal.storage.user import UserStorage
from internal.storage.recipe import RecipeStorage
from internal.service.fastapi.middleware.cors import add_cors_middleware
from internal.service.fastapi.middleware.authenticate import add_authenticate_middleware, get_user_from_request
from internal.service.fastapi.resources.user import UserResource
from internal.service.fastapi.resources.recipe import RecipeResource
from internal.service.fastapi.schemas import BaseResponse
from internal.service.fastapi.schemas.root import GetRootResponse


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

        # Add the root endpoint.
        self.__api.add_api_route("/", self._root, methods=["GET"], response_model=BaseResponse[GetRootResponse])

        # Add the API resources.
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

    async def _root(self, request_user: BaseUser = Depends(get_user_from_request)) -> BaseResponse[GetRootResponse]:
        """
        Root endpoint for the API.

        Args:
            request_user: the user making the request.

        Returns:
            a friendly response.
        """
        message = "Hello World :)"
        if request_user.is_authenticated:
            message = f"Welcome back {request_user.display_name} :)"

        try:
            # Format the response.
            data = GetRootResponse(name=self.__name, version=self.__version, message=message)
        except Exception as e:
            detail = f"Could not format response: `{str(e)}`."
            logger.error(detail, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

        logger.debug("Root finished successfully.")
        return BaseResponse(detail="Root get finished successfully.", data=data)

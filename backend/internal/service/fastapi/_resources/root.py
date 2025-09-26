import logging
from starlette.authentication import BaseUser
from fastapi import APIRouter, Depends, HTTPException, status

from internal.service.fastapi._middleware.auth import get_user_from_request
from internal.service._schemas import BaseResponse
from internal.service._schemas.root import GetRootResponse


logger = logging.getLogger(__name__)


class RootResource(APIRouter):
    """The RootResource is the API resource for recipes."""

    def __init__(self, name: str, version: str):
        """
        Initialise the RootResource.

        Args:
            name: the name of the API.
            version: the version of the API.
        """
        super().__init__()
        self.__name = name
        self.__version = version

        self.add_api_route(
            "/",
            self._get,
            methods=["GET"],
            response_model=BaseResponse[GetRootResponse]
        )

    async def _get(self, request_user: BaseUser = Depends(get_user_from_request)) -> BaseResponse[GetRootResponse]:
        """
        Get the root endpoint for the API.

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

        detail = "Root get finished successfully."
        logger.debug(detail)
        return BaseResponse(detail=detail, data=data)

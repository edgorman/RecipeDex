from dataclasses import dataclass
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.authentication import BaseUser

from internal.storage.user import UserStorage
from internal.service.fastapi.resources import BaseResponse
from internal.service.fastapi.middleware.authenticate import get_user_from_request


class UserResource(APIRouter):
    def __init__(self, user_storage_handler: UserStorage, endpoint="user"):
        super().__init__(prefix=f"/{endpoint}")
        self.__user_storage_handler = user_storage_handler

        self.add_api_route("/{user_id}", self._get, methods=["GET"])

    @dataclass
    class GetUserResponse:
        user_id: str
        user_name: str

    async def _get(
        self, user_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetUserResponse]:
        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not get user with id `{user_id}`: `user is forbidden`."
            )

        user = self.__user_storage_handler.get(user_id)
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not get user with id `{user_id}`: `it does not exist`."
            )

        return BaseResponse(
            detail="User get finished successfully.",
            data=self.GetUserResponse(
                user_id=user.display_id,
                user_name=user.display_name
            )
        )

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.authentication import BaseUser

from internal.objects.user import User
from internal.storage.user import UserStorage
from internal.service.fastapi.middleware.authenticate import get_user_from_request
from internal.service.fastapi.schemas import BaseResponse
from internal.service.fastapi.schemas.user import GetUserResponse, GetUserByProviderResponse
from internal.config.service import Service


class UserResource(APIRouter):
    def __init__(self, user_storage_handler: UserStorage, endpoint="user"):
        super().__init__(prefix=f"/{endpoint}")
        self.__user_storage_handler = user_storage_handler

        self.add_api_route("/{user_id}", self._get, methods=["GET"])
        self.add_api_route("/provider/{provider}/{provider_id}", self._get_by_provider, methods=["GET"])

    async def _get(
        self, user_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetUserResponse]:
        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {User.Action.GET.value} user with id `{user_id}`: `user is forbidden`."
            )

        user = self.__user_storage_handler.get(user_id)
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {User.Action.GET.value} user with id `{user_id}`: `it does not exist`."
            )

        return BaseResponse(
            detail=f"User {User.Action.GET.value} finished successfully.",
            data=GetUserResponse.from_objects(user)
        )

    async def _get_by_provider(
        self,
        provider: str,
        provider_id: str,
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetUserByProviderResponse]:
        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{provider}` and id `{provider_id}`: "
                       "`user is forbidden`."
            )

        try:
            provider_enum = Service.AuthProvider(provider.lower())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{provider}` and id `{provider_id}`: "
                       "`invalid provider`."
            )

        user = self.__user_storage_handler.get_by_provider_id(provider_id, provider_enum)
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{provider}` and id `{provider_id}`: "
                       "`user does not exist`."
            )

        return BaseResponse(
            detail=f"User {User.Action.GET_BY_PROVIDER.value} finished successfully.",
            data=GetUserByProviderResponse.from_objects(user)
        )

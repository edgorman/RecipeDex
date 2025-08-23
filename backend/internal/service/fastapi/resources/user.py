from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.authentication import BaseUser
from uuid import UUID

from internal.objects.user import User
from internal.storage.user import UserStorage
from internal.auth.user import UserAuthorize
from internal.service.fastapi.middleware.authenticate import get_user_from_request
from internal.service.fastapi.schemas import BaseRequest, BaseResponse
from internal.service.fastapi.schemas.user import (
    GetUserResponse, GetUserByProviderResponse, UpdateUserRequest, UpdateUserResponse, DeleteUserResponse
)


class UserResource(APIRouter):

    def __init__(self, user_storage_handler: UserStorage, user_authorize_handler: UserAuthorize, endpoint="user"):
        super().__init__(prefix=f"/{endpoint}")
        self.__user_storage_handler = user_storage_handler
        self.__user_authorize_handler = user_authorize_handler

        self.add_api_route("/{user_id}", self._get, methods=["GET"])
        self.add_api_route("/provider/{provider}/{provider_id}", self._get_by_provider, methods=["GET"])
        self.add_api_route("/{user_id}", self._update, methods=["PUT"])
        self.add_api_route("/{user_id}", self._delete, methods=["DELETE"])

    def __preprocess(self, user_id: str, request_user: User, request_action: User.Action) -> User:
        try:
            user_uuid = UUID(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {request_action.value} user with id `{user_id}`: `invalid user id, {str(e)}`."
            )

        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {request_action.value} user with id `{user_id}`: `user is forbidden`."
            )

        user = self.__user_storage_handler.get(user_uuid)
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {request_action.value} user with id `{user_id}`: `it does not exist`."
            )

        authorized = self.__user_authorize_handler.authorize(user, request_action, request_user)
        if not authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {request_action.value} user with id `{user_id}`: `user is forbidden`."
            )

        return user

    async def _get(
        self, user_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetUserResponse]:
        user = self.__preprocess(user_id, request_user, User.Action.GET)

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
            provider_enum = User.ProviderType(provider.lower())
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

    async def _update(
        self,
        request: BaseRequest[UpdateUserRequest],
        user_id: str,
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[UpdateUserResponse]:
        user = self.__preprocess(user_id, request_user, User.Action.UPDATE)

        try:
            if request.data is None:
                raise ValueError("request body missing data")
            if all([field is None for field in asdict(request.data).keys()]):
                raise ValueError("request body fields are all null")

            for field, value in asdict(request.data).items():
                if not hasattr(user, field):
                    raise ValueError(f"field {field} does not exist in User")
                if value is None:
                    continue

                try:
                    setattr(user, field, value)
                except Exception as e:
                    raise ValueError(f"bad value for User.{field}, `{value}`: {str(e)}")
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {User.Action.UPDATE.value} user: `{e}`."
            )

        try:
            self.__user_storage_handler.update(user.id, user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {User.Action.UPDATE.value} user with id `{user_id}`: `{e}`."
            )

        return BaseResponse(
            detail=f"User {User.Action.UPDATE.value} finished successfully.",
            data=UpdateUserResponse.from_objects(user)
        )

    async def _delete(
        self, user_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[DeleteUserResponse]:
        user = self.__preprocess(user_id, request_user, User.Action.DELETE)

        try:
            self.__user_storage_handler.delete(user.id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {User.Action.DELETE.value} user with id `{user_id}`: `{e}`."
            )

        return BaseResponse(
            detail=f"User {User.Action.DELETE.value} finished successfully.",
            data=DeleteUserResponse.from_objects(user)
        )

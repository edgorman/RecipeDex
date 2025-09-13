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
    """The UserResource is the API resource for users."""

    def __init__(self, user_storage_handler: UserStorage, user_authorize_handler: UserAuthorize, endpoint="user"):
        """
        Initialise the UserResource.

        Args:
            user_storage_handler: the handler for user storage.
            user_authorize_handler: the handler for user authorization.
            endpoint: the endpoint to mount the resource on.
        """
        super().__init__(prefix=f"/{endpoint}")
        self.__user_storage_handler = user_storage_handler
        self.__user_authorize_handler = user_authorize_handler

        # Add the API routes for the resource.
        self.add_api_route(
            "/{user_id}",
            self._get,
            methods=["GET"],
            response_model=BaseResponse[GetUserResponse]
        )
        self.add_api_route(
            "/provider/{provider}/{provider_id}",
            self._get_by_provider,
            methods=["GET"],
            response_model=BaseResponse[GetUserByProviderResponse]
        )
        self.add_api_route(
            "/{user_id}",
            self._update,
            methods=["PUT"],
            response_model=BaseResponse[UpdateUserResponse]
        )
        self.add_api_route(
            "/{user_id}",
            self._delete,
            methods=["DELETE"],
            response_model=BaseResponse[DeleteUserResponse]
        )

    def __preprocess(self, user_id: str, request_user: User, request_action: User.Action) -> User:
        """
        Preprocess a request by validating the user ID, checking for existence, and authorizing the user.

        Args:
            user_id: the ID of the user to preprocess.
            request_user: the user making the request.
            request_action: the action being performed.

        Returns:
            the user if it exists and the user is authorized.

        Raises:
            HTTPException: if the user ID is invalid, the user does not exist, or the user is not authorized.
        """
        try:
            # Validate the user ID.
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

        # Get the user from storage.
        user = self.__user_storage_handler.get(user_uuid)
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {request_action.value} user with id `{user_id}`: `it does not exist`."
            )

        # Authorize the user for the action.
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
        """
        Get a user by ID.

        Args:
            user_id: the ID of the user to get.
            request_user: the user making the request.

        Returns:
            the user.
        """
        user = self.__preprocess(user_id, request_user, User.Action.GET)

        try:
            # Format the response.
            data = GetUserResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"User {User.Action.GET.value} finished successfully.", data=data)

    async def _get_by_provider(
        self,
        provider: str,
        provider_id: str,
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[GetUserByProviderResponse]:
        """
        Get a user by provider and provider ID.

        Args:
            provider: the provider to get the user by.
            provider_id: the provider ID to get the user by.
            request_user: the user making the request.

        Returns:
            the user.
        """
        if not request_user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{provider}` and id `{provider_id}`: "
                       "`user is forbidden`."
            )

        try:
            # Validate the provider.
            provider_enum = User.ProviderType(provider.lower())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{provider}` and id `{provider_id}`: "
                       "`invalid provider`."
            )

        # Get the user from storage.
        user = self.__user_storage_handler.get_by_provider_id(provider_id, provider_enum)
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not {User.Action.GET_BY_PROVIDER.value} for `{provider}` and id `{provider_id}`: "
                       "`user does not exist`."
            )

        try:
            # Format the response.
            data = GetUserByProviderResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"User {User.Action.GET_BY_PROVIDER.value} finished successfully.", data=data)

    async def _update(
        self,
        request: BaseRequest[UpdateUserRequest],
        user_id: str,
        request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[UpdateUserResponse]:
        """
        Update a user.

        Args:
            request: the request to update the user.
            user_id: the ID of the user to update.
            request_user: the user making the request.

        Returns:
            the updated user.
        """
        user = self.__preprocess(user_id, request_user, User.Action.UPDATE)

        try:
            # Update the user object from the request data.
            data = request.data.model_dump()

            if all([field is None for field in data.values()]):
                raise ValueError("all data fields cannot be null")

            for field, value in data.items():
                if value is None:
                    continue

                try:
                    setattr(user, field, value)
                except Exception as e:
                    raise ValueError(f"bad value for User.{field}, `{value}`: {str(e)}")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not {User.Action.UPDATE.value} user: `{e}`."
            )

        try:
            # Update the user in storage.
            self.__user_storage_handler.update(user.id, user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {User.Action.UPDATE.value} user with id `{user_id}`: `{e}`."
            )

        try:
            # Format the response.
            data = UpdateUserResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"User {User.Action.UPDATE.value} finished successfully.", data=data)

    async def _delete(
        self, user_id: str, request_user: BaseUser = Depends(get_user_from_request)
    ) -> BaseResponse[DeleteUserResponse]:
        """
        Delete a user.

        Args:
            user_id: the ID of the user to delete.
            request_user: the user making the request.

        Returns:
            the deleted user.
        """
        user = self.__preprocess(user_id, request_user, User.Action.DELETE)

        try:
            # Delete the user from storage.
            self.__user_storage_handler.delete(user.id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not {User.Action.DELETE.value} user with id `{user_id}`: `{e}`."
            )

        try:
            # Format the response.
            data = DeleteUserResponse.model_validate(user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not format response: `{str(e)}`."
            )

        return BaseResponse(detail=f"User {User.Action.DELETE.value} finished successfully.", data=data)

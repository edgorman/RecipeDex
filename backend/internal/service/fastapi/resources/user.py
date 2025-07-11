from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from internal.storage.user import UserStorage


class UserResource(APIRouter):
    def __init__(self, user_storage_handler: UserStorage, endpoint="user"):
        super().__init__(prefix=f"/{endpoint}")
        self.__user_storage_handler = user_storage_handler

        self.add_api_route("/{user_id}", self._get, methods=["GET"])

    async def _get(self, request: Request, user_id: str):
        if not request.user.is_authenticated:
            raise HTTPException(
                status_code=403,
                detail=f"Could not get user with id `{user_id}`: `user is not authorized`."
            )

        user = self.__user_storage_handler.get(user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not get user with id `{user_id}`: `it does not exist`."
            )

        return JSONResponse(
            {
                "id": user.display_id,
                "display_name": user.display_name,
            }
        )

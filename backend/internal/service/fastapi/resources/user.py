from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from internal.storage.user import UserStorage


USER_RESOURCE_ENDPOINT = "user"


class UserResource(APIRouter):
    def __init__(self, user_storage_handler: UserStorage):
        super().__init__(prefix=f"/{USER_RESOURCE_ENDPOINT}")
        self.__user_storage_handler = user_storage_handler

        self.add_api_route("/{user_id}", self._get, methods=["GET"])

    async def _get(self, _: Request, user_id: str):
        user = self.__user_storage_handler.get(user_id)

        if user is None:
            return JSONResponse(
                {
                    "reason": f"user resource with id {user_id} not found"
                },
                status_code=404
            )

        return JSONResponse(
            {
                "id": user.id,
                "display_name": user.display_name,
            }
        )

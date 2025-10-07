from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class GetUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class GetUserByProviderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None


class UpdateUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class DeleteUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

from uuid import UUID
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict

from internal.objects.recipe import Recipe
from internal.objects.session import Session


class ListRecipesItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    private: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class ListRecipesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recipes: List[ListRecipesItem]


class GetRecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    ingredients: List[Recipe.Ingredient]
    instructions: List[Recipe.Instruction]


class GetMetadataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    private: bool
    user_session_mapping: Dict[UUID, str]
    user_role_mapping: Dict[UUID, Recipe.Role]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class CreateRecipeRequest(BaseModel):
    name: Optional[str] = "Untitled Recipe"
    private: Optional[bool] = False


class CreateRecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class UpdateRecipeRequest(BaseModel):
    # id is passed in the request url
    name: Optional[str] = None
    private: Optional[bool] = None
    user_role_mapping: Optional[Dict[UUID, str]] = None
    ingredients: Optional[List[Recipe.Ingredient]] = None
    instructions: Optional[List[Recipe.Instruction]] = None


class UpdateRecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class DeleteRecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class GetMessagesItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: Session.Message.Role
    value: Optional[str]
    tool: Optional[Session.Message.ToolResponse]
    created_at: datetime


class GetMessagesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    messages: List[GetMessagesItem]


class SendMessageRequest(BaseModel):
    value: str


class SendMessageResponse(Session.Message):
    model_config = ConfigDict(from_attributes=True)

    role: Session.Message.Role
    value: Optional[str]
    tool: Optional[Session.Message.ToolResponse]
    created_at: datetime

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import UUID

from internal.objects.recipe import Recipe


@dataclass
class ListRecipesItem:
    id: UUID
    name: str
    private: bool

    @classmethod
    def from_objects(cls, recipe: Recipe) -> "ListRecipesItem":
        """Create a ListRecipesItem from a Recipe object"""
        return cls(
            id=recipe.display_id,
            name=recipe.display_name,
            private=recipe.private
        )


@dataclass
class ListRecipesResponse:
    recipes: List[ListRecipesItem]

    @classmethod
    def from_objects(cls, recipes: List[Recipe]) -> "ListRecipesResponse":
        """Create a ListRecipesResponse from a list of Recipe objects"""
        return cls(
            recipes=[
                ListRecipesItem.from_objects(recipe) for recipe in recipes
            ]
        )


@dataclass
class GetRecipeResponse:
    id: UUID
    name: str
    ingredients: List[Dict[str, Any]]
    instructions: List[Dict[str, Any]]

    @classmethod
    def from_objects(cls, recipe: Recipe) -> "GetRecipeResponse":
        """Create a GetRecipeResponse from a Recipe object"""
        return cls(
            id=recipe.display_id,
            name=recipe.display_name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions
        )


@dataclass
class GetMetadataResponse:
    id: UUID
    deleted: bool
    private: bool
    user_session_mapping: Dict[str, str]
    user_role_mapping: Dict[str, str]

    @classmethod
    def from_objects(cls, recipe: Recipe) -> "GetMetadataResponse":
        """Create a GetMetadataResponse from a Recipe object"""
        return cls(
            id=recipe.display_id,
            deleted=recipe.deleted,
            private=recipe.private,
            user_session_mapping={str(key): value for key, value in recipe.user_session_mapping.items()},
            user_role_mapping={str(key): role.value for key, role in recipe.user_role_mapping.items()}
        )


@dataclass
class CreateRecipeRequest:
    name: Optional[str] = "Untitled Recipe"
    private: Optional[bool] = False

    @classmethod
    def from_objects(cls, data: dict) -> "CreateRecipeRequest":
        """Create an CreateRecipeRequest from a dict object"""
        return cls(
            name=data.get("name"),
            private=data.get("private")
        )


@dataclass
class CreateRecipeResponse:
    id: UUID

    @classmethod
    def from_objects(cls, recipe: Recipe) -> "CreateRecipeResponse":
        """Create a CreateRecipeResponse from a Recipe object"""
        return cls(id=recipe.display_id)


@dataclass
class UpdateRecipeRequest:
    name: Optional[str] = None
    private: Optional[bool] = None
    user_role_mapping: Optional[Dict[str, str]] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None


@dataclass
class UpdateRecipeResponse:
    id: UUID

    @classmethod
    def from_objects(cls, recipe: Recipe) -> "UpdateRecipeResponse":
        """Create a UpdateRecipeResponse from a Recipe object"""
        return cls(id=recipe.display_id)


@dataclass
class DeleteRecipeResponse:
    id: UUID

    @classmethod
    def from_objects(cls, recipe: Recipe) -> "DeleteRecipeResponse":
        """Create a DeleteRecipeResponse from a Recipe object"""
        return cls(id=recipe.display_id)


@dataclass
class GetMessageItem:
    role: Recipe.Role
    value: str

    @classmethod
    def from_objects(cls, message: Recipe.Message) -> "GetMessageItem":
        """Create a GetMessageItem from a Recipe Message object"""
        return cls(
            role=message.role,
            value=message.value
        )


@dataclass
class GetMessagesResponse:
    messages: List[GetMessageItem]

    @classmethod
    def from_objects(cls, messages: List[Recipe.Message]) -> "GetMessagesResponse":
        """Create a GetMessagesResponse from a list of Recipe Message objects"""
        return cls(
            messages=[
                GetMessageItem.from_objects(message) for message in messages
            ]
        )


@dataclass
class SendMessageRequest:
    value: str

    @classmethod
    def from_objects(cls, data: dict) -> "SendMessageRequest":
        """Create a SendMessageRequest from generic dict object"""
        return cls(
            value=data["value"]
        )


@dataclass
class SendMessageResponse:
    role: str
    value: str

    @classmethod
    def from_objects(cls, message: Recipe.Message) -> "SendMessageResponse":
        """Create a SendMessageResponse from a Recipe Message object"""
        return cls(
            role=message.role,
            value=message.value
        )

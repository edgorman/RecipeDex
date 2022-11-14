
from typing import Optional
from pydantic import (
    Field,
    BaseModel,
    ConstrainedStr,
    ConstrainedList,
)


class HostnameSchema(BaseModel):
    hostname: str = ConstrainedStr(to_lower=True)

    class Config:
        schema_extra = {
            "example": {
                "hostname": "https://bbcgoodfood.com"
            }
        }


class RecipeSchema(BaseModel):
    hostname_id: int = Field(...)
    hostname_path: ConstrainedStr(to_lower=True)
    name = ConstrainedStr(min_length=1)
    tags = ConstrainedList(str, min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "hostname_id": 1,
                "hostname_path": "/path/to/recipe",
                "name": "recipe name",
                "tags": ["separate", "tags"]
            }
        }


class UpdateRecipeModel(BaseModel):
    hostname_id: int = Optional[Field(...)]
    hostname_path: Optional[ConstrainedStr(to_lower=True)]
    name = Optional[ConstrainedStr(min_length=1)]
    tags = Optional[ConstrainedList(str, min_items=1)]

    class Config:
        schema_extra = {
            "example": {
                "hostname_id": 1,
                "hostname_path": "/path/to/recipe",
                "name": "recipe name",
                "tags": ["separate", "tags"]
            }
        }

from typing import Optional
from pydantic import (
    Field,
    BaseModel,
    constr,
    conlist,
)


# Define the models used
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


class RecipeSchema(BaseModel):
    url: str = constr(to_lower=True)
    name: str = constr(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "url": "/path/to/recipe",
                "name": "recipe name",
            }
        }
    
    def helper(recipe) -> dict:
        return {
            "id": str(recipe["_id"]),
            "url": recipe["url"],
            "name": recipe["name"],
        }

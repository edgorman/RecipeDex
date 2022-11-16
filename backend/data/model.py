from pydantic import (
    BaseModel,
    constr,
    conset,
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


class TagSchema(BaseModel):
    tag: str = constr(to_lower=True)
    recipe_ids: set = conset(str, min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "tag": "chicken",
                "recipe_ids": {
                    "63753dcc352382d88723cb90",
                    "63753dcc352382d88723cb91",
                },
            }
        }

    def helper(tag) -> dict:
        return {
            "id": str(tag["_id"]),
            "tag": tag["tag"],
            "recipe_ids": tag["recipe_ids"],
        }

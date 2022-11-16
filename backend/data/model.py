from pydantic import (
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


class TagSchema(BaseModel):
    tag: str = constr(to_lower=True)
    recipe_ids: list = conlist(str, min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "tag": "chicken",
                "recipe_ids": [
                    "51651651651",
                    "75646846154",
                ],
            }
        }

    def helper(tag) -> dict:
        return {
            "id": str(tag["_id"]),
            "tag": tag["tag"],
            "recipe_ids": tag["recipe_ids"],
        }

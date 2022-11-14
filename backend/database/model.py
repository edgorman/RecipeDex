from typing import Optional
from pydantic import (
    Field,
    BaseModel,
    constr,
    conlist,
)


# # Define the schemas used
# class HostnameSchema(BaseModel):
#     hostname: str = constr(to_lower=True)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "hostname": "https://bbcgoodfood.com"
#             }
#         }
    
#     def helper(hostname) -> dict:
#         return {
#             "id": str(hostname["_id"]),
#             "hostname": hostname["hostname"],
#         }


class RecipeSchema(BaseModel):
    path: str = constr(to_lower=True)
    name: str = constr(min_length=1)
    tags: list = conlist(str, min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "path": "/path/to/recipe",
                "name": "recipe name",
                "tags": ["separate", "tags"]
            }
        }
    
    def helper(recipe) -> dict:
        return {
            "id": str(recipe["_id"]),
            "path": recipe["path"],
            "name": recipe["name"],
            "tags": recipe["tags"],
        }


# Define the models used
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

import logging
from fastapi import Query
from fastapi import APIRouter
from bson.objectid import ObjectId

from backend.data.model import ResponseModel
from backend.data.database import get_tags
from backend.data.database import get_recipes


logger = logging.getLogger("backend.api.routers.search")


router = APIRouter(
    prefix='/search',
    tags=['search']
)


@router.get("/", response_description="Get all recipes by search terms")
async def get_recipes_by_search(t: list[str] | None = Query(default=None)):
    tags = await get_tags({"tag": {"$in": t}})
    recipe_ids = list(set(sum([t["recipe_ids"] for t in tags], [])))
    object_ids = [ObjectId(i) for i in recipe_ids]
    recipes = await get_recipes({"_id": {"$in": object_ids}})

    if recipes:
        return ResponseModel(recipes, "Recipe data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")

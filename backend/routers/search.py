import logging
from fastapi import Query
from fastapi import Request
from fastapi import APIRouter
from bson.objectid import ObjectId

from backend import limiter
from backend.data.model import ResponseModel
from backend.data.database import get_tags
from backend.data.database import get_recipes


logger = logging.getLogger("backend.api.routers.search")

# Set up search router
router = APIRouter(
    prefix='/search',
    tags=['search']
)


@router.get("/", response_description="Get all recipes by search terms")
@limiter.exempt
async def get_recipes_by_search(request: Request, limit: int | None = 12, t: list[str] | None = Query(default=None)):
    tags = await get_tags({"tag": {"$in": t}})
    recipe_ids = list(set(sum([t["recipe_ids"] for t in tags], [])))[:limit]
    object_ids = [ObjectId(i) for i in recipe_ids]
    recipes = await get_recipes({"_id": {"$in": object_ids}})

    if recipes:
        return ResponseModel(recipes, "Search data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")

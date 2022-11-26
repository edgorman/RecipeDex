import json
import asyncio
import logging
from slowapi import Limiter
from fastapi import Request
from fastapi import APIRouter
from argparse import Namespace
from slowapi.util import get_remote_address

from recipedex import App
from backend import limiter
from backend.data.model import ResponseModel
from backend.data.database import add_recipe
from backend.data.database import get_recipes


logger = logging.getLogger("backend.api.routers.recipes")

# Set up Recipe router
router = APIRouter(
    prefix='/recipes',
    tags=['recipes']
)


@router.get("/", response_description="Get all recipes")
@limiter.limit("6/minute")
async def get_all_recipes(request: Request):
    recipes = await get_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipe data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/{request:path}", response_description="Scrape a recipe for a given url")
@limiter.limit("6/minute")
async def get_recipe_by_url(request: Request, unit: str | None = "default", serves: int | None = 0):
    urls = [request.url.path[9:]]
    args = Namespace(
        urls=urls,
        serves=serves,
        metric=bool(unit == "metric"),
        imperial=bool(unit == "imperial"),
        log=logging.getLevelName(logger.getEffectiveLevel()),
    )

    resp = json.loads(App.main(args))
    await asyncio.gather(*[add_recipe(url, recipe) for url, recipe in resp.items()])
    return resp

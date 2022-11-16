import json
import asyncio
import logging
from argparse import Namespace
from fastapi import Request
from fastapi import APIRouter

from recipedex import App
from backend.data.model import ResponseModel
from backend.data.database import add_recipe
from backend.data.database import get_recipes


logger = logging.getLogger("backend.api.routers.recipes")


router = APIRouter(
    prefix='/recipes',
    tags=['recipes']
)


@router.get("/", response_description="Get all recipes")
async def get_all_recipes():
    recipes = await get_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipe data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/{request:path}", response_description="Scrape a recipe for a given url")
async def get_recipe_by_url(request: Request, metric: bool = False, imperial: bool = False):
    urls = [request.url.path[9:]]
    args = Namespace(
        urls=urls,
        serves=0,
        metric=metric,
        imperial=imperial,
        log=logging.getLevelName(logger.getEffectiveLevel()),
    )

    resp = json.loads(App.main(args))
    await asyncio.gather(*[add_recipe(url, recipe) for url, recipe in resp.items()])
    return resp

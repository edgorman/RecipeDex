import json
import asyncio
import logging
from argparse import Namespace
from fastapi import Request
from fastapi import APIRouter

from recipedex import App
from backend.database.model import ResponseModel
from backend.database.database import retrieve_recipes
from backend.database.database import add_recipe


logger = logging.getLogger("backend.api.routers.recipes")


router = APIRouter(
    prefix = '/recipe',
    tags = ['recipe']
)


@router.get("/all", response_description="Retrieve all scraped urls")
async def get_recipes():
    recipes = await retrieve_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipe data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/{request:path}", response_description="Scrape a url")
async def get_recipe_by_url(request: Request, metric: bool = False, imperial: bool = False):
    urls = [request.url.path[8:]]
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

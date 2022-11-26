import json
import asyncio
import logging
from fastapi import Request
from fastapi import APIRouter
from argparse import Namespace

from recipedex import App
from backend import limiter
from backend.data.model import ResponseModel
from backend.data.database import add_recipe
from backend.data.database import get_recipes
from backend.data.database import check_cache
from backend.data.database import recent_cache


logger = logging.getLogger("backend.api.routers.recipes")

# Set up Recipe router
router = APIRouter(
    prefix='/recipes',
    tags=['recipes']
)


@router.get("/", response_description="Get all recipes")
@limiter.limit("30/minute")
async def get_all_recipes(request: Request):
    recipes = await get_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipe data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/recent", response_description="Get all recently viewed recipes")
@limiter.limit("30/minute")
async def get_recent_recipes(request: Request, limit: int | None = 6):
    recents = await recent_cache(limit)
    if recents:
        return ResponseModel(recents, "Recipe data retrieved successfully")
    return ResponseModel(recents, "Empty list returned")


# TODO: Uncomment cost function when slowapi v0.1.7 is released
@router.get("/{request:path}", response_description="Scrape a recipe for a given url")
@limiter.limit("30/minute")  # , cost=lambda request: int(await check_cache(url) is None))
async def get_recipe_by_url(request: Request, unit: str | None = "default", serves: int | None = 0):
    url = request.url.path[9:]
    cache_resp = await check_cache(url)

    if cache_resp is None:
        args = Namespace(
            urls=[url],
            serves=serves,
            metric=bool(unit == "metric"),
            imperial=bool(unit == "imperial"),
            log=logging.getLevelName(logger.getEffectiveLevel()),
        )

        resp = json.loads(App.main(args))
        await asyncio.gather(*[add_recipe(u, r) for u, r in resp.items()])
    else:
        # TODO: check serving and unit matches cache, 
        #       if not call app function manually
        resp = {url: cache_resp}
    return resp

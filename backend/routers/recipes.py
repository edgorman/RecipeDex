import json
import copy
import asyncio
import logging
from fastapi import Request
from fastapi import APIRouter
from argparse import Namespace

from recipedex import App
from recipedex.recipe import Recipe
from backend import limiter
from backend.data.model import ResponseModel


logger = logging.getLogger("backend.api.routers.recipes")

# Set up Recipe router
router = APIRouter(
    prefix='/recipes',
    tags=['recipes']
)


@router.get("/", response_description="Get all recipes")
@limiter.limit("30/minute")
async def get_all_recipes(request: Request):
    recipes = await request.app.state.db.get_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipe data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/recent", response_description="Get all recently viewed recipes")
@limiter.limit("30/minute")
async def get_recent_recipes(request: Request, limit: int | None = 6):
    recents = await request.app.state.db.recent_cache(limit)
    if recents:
        return ResponseModel(recents, "Recipe data retrieved successfully")
    return ResponseModel(recents, "Empty list returned")


@router.get("/{request:path}", response_description="Scrape a recipe for a given url")
@limiter.limit("30/minute", cost=lambda request: int(request.app.state.db.check_cache(request.url.path[9:]) is None))
async def get_recipe_by_url(request: Request, unit: str | None = "default", serves: int | None = 0):
    url = request.url.path[9:]
    cache = request.app.state.db.check_cache(url)

    # If cache does not contain the url
    if cache is None:
        # Parse the recipe using the RecipeDex module
        args = Namespace(
            urls=[url],
            serves=serves,
            metric=bool(unit == "metric"),
            imperial=bool(unit == "imperial"),
            log=logging.getLevelName(logger.getEffectiveLevel()),
        )
        recipe = {url: json.loads(App.main(args))[0]}

        # Add this recipe to the database for fast indexing
        await asyncio.gather(*[request.app.state.db.add_recipe(u, r) for u, r in recipe.items()])

    # Else the cache does contain the url
    else:
        recipe = {url: copy.deepcopy(cache)}

        # If the cached data does not match the request
        if unit != cache["unit"] or (serves > 0 and serves != cache["servings"]):
            # Generate new recipe using existing values
            recipe[url] = Recipe(
                serves=serves,
                metric=bool(unit == "metric"),
                imperial=bool(unit == "imperial"),
                **recipe[url]
            )

    return ResponseModel(recipe, "Recipe data retrieved successfully")

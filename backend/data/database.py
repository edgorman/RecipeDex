import asyncio
import logging
import pymongo
import motor.motor_asyncio
from pylru import lrucache
from bson.objectid import ObjectId

from backend.data.model import RecipeSchema
from backend.data.model import TagSchema


logger = logging.getLogger("backend.api.database.database")

# Asynchronous function template


async def call_function(func, *args) -> asyncio.coroutine:
    return await func(*args)

# Set up MongoDB connection and assign collections
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
database = client.recipedex

# Set up internal LRU cache
cache = lrucache(64)


def check_cache(url: str) -> dict:
    if url in cache:
        return cache[url]
    else:
        return None


async def recent_cache(limit: int = 6) -> dict:
    return {key: cache[key] for key in list(cache.keys())[:limit][::-1]}


# Functions for recipe collection
recipe_collection = database.get_collection("recipe_collection")
recipe_collection.create_index([("url", pymongo.DESCENDING)])


async def get_recipe(query: dict = {}) -> dict:
    try:
        result = await recipe_collection.find_one(query)

        if result:
            return RecipeSchema.helper(result)
        return None
    except Exception as e:
        logger.error(f"Could not find recipe with query '{query}': {str(e)}.")


async def add_recipe(url: str, recipe: dict):
    try:
        if await get_recipe({"url": url}) is None:
            await recipe_collection.insert_one({
                "url": url,
                "name": recipe["name"],
            })

        recipe_id = (await get_recipe({"url": url}))["id"]
        cache[url] = recipe
    except Exception as e:
        logger.error(f"Could not add recipe '{url}': {str(e)}.")
        return

    for tag in recipe["tags"]:
        try:
            await add_tag(tag, recipe_id)
        except Exception as e:
            logger.error(f"Could not add tags for recipe '{url}': {str(e)}.")


async def delete_recipe(recipe_id: str):
    try:
        await recipe_collection.delete_one({"_id": ObjectId(recipe_id)})
    except Exception as e:
        logger.error(f"Could not delete recipe '{recipe_id}': '{str(e)}'.")


async def get_recipes(query: dict = {}) -> list:
    recipes = []
    async for recipe in recipe_collection.find(query):
        try:
            recipes.append(RecipeSchema.helper(recipe))
        except Exception as e:
            logger.error(f"Could not parse recipe '{recipe}': '{str(e)}'.")
            recipes.append({})
    return recipes


async def clear_recipes():
    try:
        recipe_collection.drop()
    except Exception as e:
        logger.error(f"Could not drop recipe collection: '{str(e)}'.")


# Functions for tags collection
tag_collection = database.get_collection("tag_collection")
tag_collection.create_index([("tag", pymongo.DESCENDING)])


async def get_tag(query: dict = {}) -> dict:
    try:
        result = await tag_collection.find_one(query)

        if result:
            return TagSchema.helper(result)
        return None
    except Exception as e:
        logger.error(f"Could not find tag with query '{query}': {str(e)}.")


async def add_tag(tag: str, recipe_id: str):
    try:
        if await get_tag({"tag": tag}) is None:
            await tag_collection.insert_one({
                "tag": tag,
                "recipe_ids": [recipe_id],
            })
        else:
            await tag_collection.update_one(
                {"tag": tag},
                {"$addToSet": {"recipe_ids": recipe_id}}
            )
    except Exception as e:
        logger.error(f"Could not add recipe_id '{recipe_id}' to tag '{tag}': {str(e)}.")


async def delete_tag(tag_id: str):
    try:
        await tag_collection.delete_one({"_id": ObjectId(tag_id)})
    except Exception as e:
        logger.warning(f"Could not delete tag '{tag_id}': '{str(e)}'.")


async def get_tags(query: dict = {}) -> list:
    tags = []
    async for tag in tag_collection.find(query):
        try:
            tags.append(TagSchema.helper(tag))
        except Exception as e:
            logger.warning(f"Could not parse tag '{tag}': '{str(e)}'.")
            tags.append({})
    return tags


async def clear_tags():
    try:
        tag_collection.drop()
    except Exception as e:
        logger.error(f"Could not drop tag collection: '{str(e)}'.")

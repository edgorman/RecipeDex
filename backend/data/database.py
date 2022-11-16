import asyncio
import logging
import pymongo
import motor.motor_asyncio
from bson.objectid import ObjectId

from backend.data.model import RecipeSchema
from backend.data.model import TagSchema


logger = logging.getLogger("backend.api.database.database")


# Set up MongoDB connection and assign collections
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
database = client.recipedex


# Asynchronous function template
async def call_function(func) -> asyncio.coroutine:
    await func()


# Functions for recipe collection
recipe_collection = database.get_collection("recipe_collection")
recipe_collection.create_index([("url", pymongo.DESCENDING)])

async def get_recipe(key: str="url", value: str="") -> dict:
    try:
        result = await recipe_collection.find_one({key: value})

        if result:
            return RecipeSchema.helper(result)
        return None
    except Exception as e:
        logger.error(f"Could not find key '{key}' with value '{value}': {str(e)}.")


async def add_recipe(url: str, recipe: dict):
    try:
        if await get_recipe("url", url) is None:
            await recipe_collection.insert_one({
                "url": url,
                "name": recipe["name"],
            })

        recipe_id = (await get_recipe("url", url))["id"]
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


async def get_recipes(key: str="url", value: str="") -> list:
    recipes = []
    query = {} if value == "" else {key: value}

    async for recipe in recipe_collection.find(query):
        try:
            recipes.append(
                RecipeSchema.helper(recipe)
            )
        except Exception as e:
            logger.error(f"Could not get all recipes: '{str(e)}'.")
            recipes.append({})
    return recipes
    


async def clear_recipes():
    recipes = await get_recipes()

    for recipe in recipes:
        try:
            await delete_recipe(recipe["id"])
        except Exception as e:
            logger.error(f"Could not clear all recipes: '{str(e)}'.")


# Functions for tags collection
tag_collection = database.get_collection("tag_collection")
tag_collection.create_index([("tag", pymongo.DESCENDING)])

async def get_tag(key: str="tag", value: str="") -> dict:
    try:
        result = await tag_collection.find_one({key: value})

        if result:
            return TagSchema.helper(result)
        return None
    except Exception as e:
        logger.error(f"Could not find key '{key}' with value '{value}': {str(e)}.")


async def add_tag(tag: str, recipe_id: str):
    try:
        if await get_tag("tag", tag) is None:
            await tag_collection.insert_one({
                "tag": tag,
                "recipe_ids": [recipe_id],
            })
        else:
            await tag_collection.update_one(
                {"tag": tag},
                {"$addToSet": {"recipe_ids": recipe_id}},
                upsert = True
            )
    except Exception as e:
        logger.error(f"Could not add recipe_id '{recipe_id}' to tag '{tag}': {str(e)}.")


async def delete_tag(tag_id: str):
    try:
        await tag_collection.delete_one({"_id": ObjectId(tag_id)})
    except Exception as e:
        logger.warning(f"Could not delete tag '{tag_id}': '{str(e)}'.")


async def get_tags(key: str="tag", value: str="") -> list:
    tags = []
    query = {} if value == "" else {key: value}

    async for tag in tag_collection.find(query):
        try:
            tags.append(
                TagSchema.helper(tag)
            )
        except Exception as e:
            logger.warning(f"Could not get all tags: '{str(e)}'.")
            tags.append({})
    return tags


async def clear_tags():
    tags = await get_tags()

    for tag in tags:
        try:
            await delete_tag(tag["id"])
        except Exception as e:
            logger.error(f"Could not clear all tags: '{str(e)}'.")

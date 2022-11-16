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

async def get_recipe(key: str = "url", value: str = "") -> dict:
    try:
        return await recipe_collection.find_one({key: value})
    except Exception as e:
        logger.warning(f"Could not find key '{key}' with value '{value}': {str(e)}.")


async def add_recipe(url: str, recipe: dict):
    try:
        if not await recipe_collection.find_one({"url": url}):
            await recipe_collection.insert_one({
                "url": url,
                "name": recipe["name"],
            })
    except Exception as e:
        logger.warning(f"Could not add recipe '{url}': {str(e)}.")


async def delete_recipe(recipe_id: str):
    try:
        await recipe_collection.delete_one({"_id": ObjectId(recipe_id)})
    except Exception as e:
        logger.warning(f"Could not delete recipe '{recipe_id}': '{str(e)}'.")


async def all_recipes() -> list:
    try:
        recipes = []
        async for recipe in recipe_collection.find():
            recipes.append(
                RecipeSchema.helper(recipe)
            )
        return recipes
    except Exception as e:
        logger.warning(f"Could not get all recipes: '{str(e)}'.")


async def clear_recipes():
    try:
        recipes = await all_recipes()
        for recipe in recipes:
            await delete_recipe(recipe["id"])
    except Exception as e:
        logger.warning(f"Could not clear all recipes: '{str(e)}'.")


# Functions for tags collection
tag_collection = database.get_collection("tag_collection")
tag_collection.create_index([("tag", pymongo.DESCENDING)])

async def get_tag(key: str = "tag", value: str = "") -> dict:
    try:
        return await recipe_collection.find_one({key: value})
    except Exception as e:
        logger.warning(f"Could not find key '{key}' with value '{value}': {str(e)}.")


async def add_tag(tag: str, recipe_id: str):
    try:
        if not await tag_collection.find_one({"tag": tag}):
            await recipe_collection.insert_one({
                "tag": tag,
                "recipe_ids": [recipe_id],
            })
        else:
            await tag_collection.update(
                {"tag": tag},
                {"$push": {"recipe_ids": recipe_id},
            })
    except Exception as e:
        logger.warning(f"Could not add recipe_id '{recipe_id}' to tag '{tag}': {str(e)}.")


async def delete_tag(tag_id: str):
    try:
        await tag_collection.delete_one({"_id": ObjectId(tag_id)})
    except Exception as e:
        logger.warning(f"Could not delete tag '{tag_id}': '{str(e)}'.")


async def all_tags() -> list:
    try:
        tags = []
        async for tag in tag_collection.find():
            tags.append(
                TagSchema.helper(tag)
            )
        return tags
    except Exception as e:
        logger.warning(f"Could not get all tags: '{str(e)}'.")


async def clear_tags():
    try:
        pass
    except Exception as e:
        logger.warning(f"Could not clear all tags: '{str(e)}'.")

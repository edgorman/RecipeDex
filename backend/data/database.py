import asyncio
import logging
import pymongo
import motor.motor_asyncio
from bson.objectid import ObjectId

from backend.data.model import RecipeSchema


logger = logging.getLogger("backend.api.database.database")


# Set up MongoDB connection and assign collections
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
database = client.recipedex
recipe_collection = database.get_collection("recipe_collection")
recipe_collection.create_index([("url", pymongo.DESCENDING)])


async def call_function(func) -> asyncio.coroutine:
    await func()


async def get_recipes() -> list:
    recipes = []
    async for recipe in recipe_collection.find():
        recipes.append(
            RecipeSchema.helper(recipe)
        )
    return recipes


async def add_recipe(url: str, recipe: dict):
    recipe_data = {
        "url": url,
        "name": recipe["name"],
    }
    try:
        recipe = await recipe_collection.insert_one(recipe_data)
        new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
    except Exception as e:
        logger.warning(f"Could not add recipe: '{recipe_data}', {str(e)}.")


async def delete_recipe(recipe_id: str):
    try:
        await recipe_collection.delete_one({"_id": ObjectId(recipe_id)})
    except Exception as e:
        logger.warning(f"Could not delete recipe: '{recipe_id}', '{str(e)}'.")


async def clear_recipes():
    recipes = await get_recipes()
    for recipe in recipes:
        await delete_recipe(recipe["id"])

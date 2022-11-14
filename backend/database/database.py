import logging
import motor.motor_asyncio
from bson.objectid import ObjectId

from backend.database.model import RecipeSchema


logger = logging.getLogger("backend.api.database.database")


# Set up MongoDB connection and assign collections
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
database = client.recipes
recipes_collection = database.get_collection("recipes_collection")


async def retrieve_recipes() -> list:
    recipes = []
    async for recipe in recipes_collection.find():
        recipes.append(
            RecipeSchema.helper(recipe)
        )
    return recipes


async def add_recipe(url: str, recipe: dict):
    recipe_data = {
        "path": url,
        "name": recipe["name"],
        "tags": [],
    }
    try:
        recipe = await recipes_collection.insert_one(recipe_data)
        new_recipe = await recipes_collection.find_one({"_id": recipe.inserted_id})
    except Exception as e:
        logger.warning(f"Could not add recipe: '{recipe_data}', {str(e)}.")


async def delete_recipe(recipe_id: str):
    try:
        await recipes_collection.delete_one({"_id": ObjectId(recipe_id)})
    except Exception as e:
        logger.warning(f"Could not delete recipe: '{recipe_id}', '{str(e)}'.")


async def clear_recipes():
    recipes = await retrieve_recipes()
    for recipe in recipes:
        print(recipe)
        await delete_recipe(recipe["id"])

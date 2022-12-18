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


class Database:

    def __init__(self, url="mongodb://127.0.0.1:27017"):
        # Set up MongoDB connection and assign collections
        self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.database = self.client.recipedex

        # Recipe table
        self.recipe_collection = self.database.get_collection("recipe_collection")
        self.recipe_collection.create_index([("url", pymongo.DESCENDING)])

        # Tags table
        self.tag_collection = self.database.get_collection("tag_collection")
        self.tag_collection.create_index([("tag", pymongo.DESCENDING)])

        # Set up internal LRU cache
        self.cache = lrucache(64)

    # Cache methods
    def check_cache(self, url: str) -> dict:
        if url in self.cache:
            return self.cache[url]
        else:
            return None

    async def recent_cache(self, limit: int = 6) -> dict:
        return {key: self.cache[key] for key in list(self.cache.keys())[:limit][::-1]}

    # Recipe methods
    async def get_recipe(self, query: dict = {}) -> dict:
        try:
            result = await self.recipe_collection.find_one(query)

            if result:
                return RecipeSchema.helper(result)
            return None
        except Exception as e:
            logger.error(f"Could not find recipe with query '{query}': {str(e)}.")

    async def add_recipe(self, url: str, recipe: dict):
        try:
            if await self.get_recipe({"url": url}) is None:
                await self.recipe_collection.insert_one({
                    "url": url,
                    "name": recipe["name"],
                })

            recipe_id = (await self.get_recipe({"url": url}))["id"]
            self.cache[url] = recipe
        except Exception as e:
            logger.error(f"Could not add recipe '{url}': {str(e)}.")
            return

        for tag in recipe["tags"]:
            try:
                await self.add_tag(tag, recipe_id)
            except Exception as e:
                logger.error(f"Could not add tags for recipe '{url}': {str(e)}.")

    async def delete_recipe(self, recipe_id: str):
        try:
            await self.recipe_collection.delete_one({"_id": ObjectId(recipe_id)})
        except Exception as e:
            logger.error(f"Could not delete recipe '{recipe_id}': '{str(e)}'.")


    async def get_recipes(self, query: dict = {}) -> list:
        recipes = []
        async for recipe in self.recipe_collection.find(query):
            try:
                recipes.append(RecipeSchema.helper(recipe))
            except Exception as e:
                logger.error(f"Could not parse recipe '{recipe}': '{str(e)}'.")
                recipes.append({})
        return recipes


    async def clear_recipes(self):
        try:
            self.recipe_collection.drop()
        except Exception as e:
            logger.error(f"Could not drop recipe collection: '{str(e)}'.")

    # Tag methods
    async def get_tag(self, query: dict = {}) -> dict:
        try:
            result = await self.tag_collection.find_one(query)

            if result:
                return TagSchema.helper(result)
            return None
        except Exception as e:
            logger.error(f"Could not find tag with query '{query}': {str(e)}.")


    async def add_tag(self, tag: str, recipe_id: str):
        try:
            if await self.get_tag({"tag": tag}) is None:
                await self.tag_collection.insert_one({
                    "tag": tag,
                    "recipe_ids": [recipe_id],
                })
            else:
                await self.tag_collection.update_one(
                    {"tag": tag},
                    {"$addToSet": {"recipe_ids": recipe_id}}
                )
        except Exception as e:
            logger.error(f"Could not add recipe_id '{recipe_id}' to tag '{tag}': {str(e)}.")


    async def delete_tag(self, tag_id: str):
        try:
            await self.tag_collection.delete_one({"_id": ObjectId(tag_id)})
        except Exception as e:
            logger.warning(f"Could not delete tag '{tag_id}': '{str(e)}'.")


    async def get_tags(self, query: dict = {}) -> list:
        tags = []
        async for tag in self.tag_collection.find(query):
            try:
                tags.append(TagSchema.helper(tag))
            except Exception as e:
                logger.warning(f"Could not parse tag '{tag}': '{str(e)}'.")
                tags.append({})
        return tags


    async def clear_tags(self):
        try:
            self.tag_collection.drop()
        except Exception as e:
            logger.error(f"Could not drop tag collection: '{str(e)}'.")

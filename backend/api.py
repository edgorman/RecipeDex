import json
import logging
import motor.motor_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import __description__
from backend import __version__
from backend import __name__
from backend.routers import recipes


logger = logging.getLogger("backend.api")

# Set up FastAPI service
api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.include_router(recipes.router)

# Set up MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
database = client.recipes
recipes_collection = database.get_collection("recipes_collection")
hostname_collection = database.get_collection("hostname_collection")

# Default
@api.get("/")
async def root():
    return {
        "name": __name__,
        "version": __version__,
        "description": __description__
    }

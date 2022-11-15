import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import __name__
from backend import __version__
from backend import __description__
from backend.routers.recipe import router as recipe_router


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
api.include_router(recipe_router)

@api.get("/")
async def root():
    return {
        "name": __name__,
        "version": __version__,
        "description": __description__
    }

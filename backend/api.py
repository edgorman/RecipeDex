import os
import logging
from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from backend import __name__
from backend import __version__
from backend import __description__
from backend import limiter
from backend.data.database import Database
from backend.routers.tags import router as tags_router
from backend.routers.search import router as search_router
from backend.routers.recipes import router as recipes_router


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
api.state.limiter = limiter
api.add_middleware(
    SlowAPIMiddleware
)
api.include_router(tags_router)
api.include_router(search_router)
api.include_router(recipes_router)


@api.on_event("startup")
async def startup():
    api.state.db = Database(os.getenv('database_url'))

@api.get("/")
async def root():
    return {
        "name": __name__,
        "version": __version__,
        "description": __description__
    }

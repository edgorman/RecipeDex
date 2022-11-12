import json
import logging
from fastapi import FastAPI
from fastapi import Request
from argparse import Namespace
from fastapi.middleware.cors import CORSMiddleware

from recipedex import App
from backend import __description__
from backend import __version__
from backend import __name__


logger = logging.getLogger("backend.api")

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
async def root():
    return {
        "name": __name__,
        "version": __version__,
        "description": __description__
    }


@api.get("/recipe/{request:path}")
async def get_recipe_by_url(request: Request):
    urls = [request.url.path[8:]]
    args = Namespace(urls=urls, log=logging.getLevelName(logger.getEffectiveLevel()), metric=False, imperial=False)
    resp = json.loads(App.main(args))

    return resp

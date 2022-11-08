import json
import logging
from fastapi import FastAPI
from fastapi import Request
from argparse import Namespace

from recipedex import App


logger = logging.getLogger("backend.api")
api = FastAPI()


@api.get("/")
async def root():
    return {"message": "hello world"}


@api.get("/recipe/{request:path}")
async def get_recipe_by_url(request: Request):
    urls = [request.url.path[8:]]
    args = Namespace(urls=urls, log=logging.getLevelName(logger.getEffectiveLevel()))
    resp = json.loads(App.main(args))

    return resp

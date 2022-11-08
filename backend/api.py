import json
import logging
from fastapi import FastAPI
from fastapi import Request
from argparse import Namespace
from fastapi.middleware.cors import CORSMiddleware

from recipedex import App


logger = logging.getLogger("backend.api")
api = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
async def root():
    return {"message": "hello world"}


@api.get("/recipe/{request:path}")
async def get_recipe_by_url(request: Request):
    urls = [request.url.path[8:]]
    args = Namespace(urls=urls, log=logging.getLevelName(logger.getEffectiveLevel()))
    resp = json.loads(App.main(args))

    return resp

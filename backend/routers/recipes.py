import json
import logging
from fastapi import Request
from fastapi import APIRouter
from argparse import Namespace

from recipedex import App


logger = logging.getLogger("backend.api.routers.recipes")


router = APIRouter(
    prefix = '/recipe',
    tags = ['recipe']
)


@router.get("/{request:path}")
async def get_recipe_by_url(request: Request, metric: bool = False, imperial: bool = False):
    urls = [request.url.path[8:]]
    args = Namespace(
        urls=urls,
        serves=1,
        metric=metric,
        imperial=imperial,
        log=logging.getLevelName(logger.getEffectiveLevel()),
    )
    resp = json.loads(App.main(args))

    return resp

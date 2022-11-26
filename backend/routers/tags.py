import logging
from fastapi import Request
from fastapi import APIRouter

from backend import limiter
from backend.data.model import ResponseModel
from backend.data.database import get_tags


logger = logging.getLogger("backend.api.routers.tags")

# Set up tags router
router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


@router.get("/", response_description="Get all tags")
@limiter.limit("10/minute")
async def get_all_tags(request: Request):
    tags = await get_tags()
    if tags:
        return ResponseModel(tags, "Tag data retrieved successfully")
    return ResponseModel(tags, "Empty list returned")


@router.get("/{tag_name}", response_description="Get all tags for a given key")
@limiter.exempt
async def get_tags_by_key(request: Request, tag_name: str):
    tags = await get_tags({"tag": tag_name})
    if tags:
        return ResponseModel(tags, "Tag data retrieved successfully")
    return ResponseModel(tags, "Empty list returned")

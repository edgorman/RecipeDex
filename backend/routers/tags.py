import logging
from fastapi import APIRouter

from backend.data.model import ResponseModel
from backend.data.database import get_tags


logger = logging.getLogger("backend.api.routers.tags")


router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


@router.get("/", response_description="Get all tags")
async def get_all_tags():
    return await get_tags_by_key("")


@router.get("/{tag_name}", response_description="Get all tags for a given key")
async def get_tags_by_key(tag_name: str):
    tags = await get_tags("tag", tag_name)
    if tags:
        return ResponseModel(tags, "Tag data retrieved successfully")
    return ResponseModel(tags, "Empty list returned")

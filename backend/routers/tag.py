import logging
from fastapi import APIRouter

from backend.data.model import ResponseModel
from backend.data.database import get_tags


logger = logging.getLogger("backend.api.routers.tag")


router = APIRouter(
    prefix='/tag',
    tags=['tag']
)


@router.get("/all", response_description="Get all tags")
async def all():
    tags = await get_tags()
    if tags:
        return ResponseModel(tags, "Tag data retrieved successfully")
    return ResponseModel(tags, "Empty list returned")


@router.get("/{tag_name}", response_description="Get all recipes for a given tag")
async def get_recipe_by_tag(tag_name: str):
    pass

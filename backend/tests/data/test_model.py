import pytest

from backend.data.model import ResponseModel


def test_response_model():
    assert ResponseModel(None, "") == {"data": None, "code": 200, "message": ""}


def test_recipe_schema():
    pass


def test_tag_schema():
    pass

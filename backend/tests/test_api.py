
import pytest

from backend.api import root


@pytest.mark.asyncio
async def test_root():
    resp = await root()
    assert resp == {"message": "hello world"}

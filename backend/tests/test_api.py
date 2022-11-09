
import pytest

from backend import __description__
from backend import __version__
from backend import __name__
from backend.api import root


@pytest.mark.asyncio
async def test_root():
    resp = await root()
    assert resp == {
        "name": __name__,
        "version": __version__,
        "description": __description__
    }

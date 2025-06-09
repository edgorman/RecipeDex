import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from internal.config.gcp import PROJECT_ID
from internal.service.middleware.cors import add_cors_middleware


@pytest.fixture
def mock_client():
    app = FastAPI()
    add_cors_middleware(app)
    return TestClient(app)


@pytest.mark.parametrize(
    "origin,expected_status,expected_allow_origin",
    [
        ("http://localhost:3000", 200, "http://localhost:3000"),
        (f"https://{PROJECT_ID}.web.app", 200, f"https://{PROJECT_ID}.web.app"),
        (f"https://{PROJECT_ID}--feature-branch.web.app", 200, f"https://{PROJECT_ID}--feature-branch.web.app"),
        ("http://malicious.com", 400, None),
    ]
)
def test_cors_middleware(mock_client, origin, expected_status, expected_allow_origin):
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "GET"
    }
    response = mock_client.options("/", headers=headers)

    assert response.status_code == expected_status
    if expected_allow_origin:
        assert response.headers.get("access-control-allow-origin") == expected_allow_origin
        assert response.headers.get("access-control-allow-credentials") == "true"
    else:
        assert "access-control-allow-origin" not in response.headers

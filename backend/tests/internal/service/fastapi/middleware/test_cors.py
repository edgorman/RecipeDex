import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from internal.config.gcp import PROJECT_ID
from internal.service.fastapi.middleware.cors import add_cors_middleware


@pytest.mark.parametrize(
    "allowed_origin,request_origin,expected_status",
    [
        ("http://localhost:3000", "http://localhost:3000", 200),
        (f"https://{PROJECT_ID}.web.app", f"https://{PROJECT_ID}.web.app", 200),
        (f"https://{PROJECT_ID}--feature-branch.web.app", f"https://{PROJECT_ID}--feature-branch.web.app", 200),
        (f"https://{PROJECT_ID}.web.app", "http://malicious.com", 400),
    ]
)
def test_cors_middleware(allowed_origin, request_origin, expected_status):
    api = FastAPI()
    add_cors_middleware(api, allowed_origin)
    mock_client = TestClient(api)

    headers = {
        "Origin": request_origin,
        "Access-Control-Request-Method": "GET"
    }
    response = mock_client.options("/", headers=headers)

    assert response.status_code == expected_status
    if response.status_code == 200:
        assert response.headers.get("access-control-allow-origin") == allowed_origin
        assert response.headers.get("access-control-allow-credentials") == "true"
    else:
        assert "access-control-allow-origin" not in response.headers

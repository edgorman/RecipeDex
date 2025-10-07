from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient

from internal.service.fastapi._middleware.rate import add_rate_limiter_middleware


def test_rate_limiter_middleware():
    api = FastAPI()
    limit_per_minute = 5
    add_rate_limiter_middleware(api, default_limit_per_minute=limit_per_minute)

    async def root(request: Request):
        return PlainTextResponse("test")
    api.add_api_route("/", root, methods=["GET"])
    mock_client = TestClient(api)

    for i in range(10):
        expected_status = 200 if i < limit_per_minute else 429
        expected_content = "test" if i < limit_per_minute else "rate limit has been exceeded"

        response = mock_client.get("/")
        assert expected_status == response.status_code
        assert expected_content in response.text

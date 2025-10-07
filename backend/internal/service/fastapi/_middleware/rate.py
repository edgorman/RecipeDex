from fastapi import FastAPI, Request, Response, status
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


def _rate_limit_exceeded_handler(request: Request, exception: RateLimitExceeded) -> Response:
    """
    The response to requests that exceed the rate limit

    Args:
        request: the request that is exceeding the limit
        exception: the exception that was raised to call this handler

    Returns:
        the error response
    """
    response = Response(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=f"Could not perform request, rate limit has been exceeded: `{exception.detail}`."
    )
    response = request.app.state.limiter._inject_headers(response, request.state.view_rate_limit)
    return response


def add_rate_limiter_middleware(app: FastAPI, default_limit_per_minute: int = 20):
    """
    Add rate limiter middleware to the FastAPI app.

    Args:
        app: the FastAPI app.
        default_limit_per_minute: the default rate limit per minute
    """
    limiter = Limiter(key_func=get_remote_address, default_limits=[f"{default_limit_per_minute}/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

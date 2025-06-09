from fastapi import FastAPI, Request, Depends

from internal.config.service import (
    NAME as SERVICE_NAME,
    VERSION as SERVICE_VERSION
)
from internal.service.middleware.cors import add_cors_middleware
from internal.service.middleware.auth import add_auth_middleware, authenticate_request


app = FastAPI()
add_cors_middleware(app)
add_auth_middleware(app, None)


@app.get("/")
async def root():
    return {
        "name": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "message": "Hello World :)"
    }


@app.get("/protected", dependencies=[Depends(authenticate_request)])
async def protected_route(request: Request):
    return {
        "message": f"Welcome back {request.user.name} :)"
    }

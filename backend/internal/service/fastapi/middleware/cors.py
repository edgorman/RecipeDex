from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.config.service import ALLOWED_ORIGIN


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[ALLOWED_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

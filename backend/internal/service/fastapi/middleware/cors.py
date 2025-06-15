from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI, allowed_origin: str):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[allowed_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

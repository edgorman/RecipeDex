from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI, allowed_origins: List[str]):
    """
    Add CORS middleware to the FastAPI app.

    Args:
        app: the FastAPI app.
        allowed_origins: a list of allowed origins.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

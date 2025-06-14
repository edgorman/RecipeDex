from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.config.gcp import PROJECT_ID as GCP_PROJECT_ID


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
        ],
        allow_origin_regex=rf"^https:\/\/{GCP_PROJECT_ID}(--[a-zA-Z0-9-]+)?\.web\.app$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

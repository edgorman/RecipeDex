import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Set up logging for module
logging.basicConfig(
    level=logging.INFO, format='%(levelname)s:\t%(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up FastAPI service
api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
async def root():
    return {
        "name": __name__,
        "version": "0.0.1"
    }

logger.info("Successfully loaded API")

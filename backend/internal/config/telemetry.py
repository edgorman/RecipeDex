import os

from internal.config import str_to_bool


TELEMETRY_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TELEMETRY_SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
TELEMETRY_LOG_LEVEL = os.getenv("TELEMETRY_LOG_LEVEL", "info").upper()
TELEMETRY_CLOUD_ENABLED = str_to_bool(os.getenv("TELEMETRY_CLOUD_ENABLED", "true"))
TELEMETRY_TRACING_ENABLED = str_to_bool(os.getenv("TELEMETRY_TRACING_ENABLED", "true"))

TELEMETRY_UVICORN_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["default"], "level": "INFO"},
    },
}

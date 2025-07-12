import os
from enum import Enum
from abc import ABC


SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.1.0")
SERVICE_HOST = os.getenv("SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = os.getenv("SERVICE_PORT", 8080)
SERVICE_ALLOWED_ORIGIN = os.getenv("SERVICE_ALLOWED_ORIGIN")
SERVICE_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

SERVICE_AUTH_SCOPE = os.getenv("SERVICE_AUTH_SCOPE", "auth")
SERVICE_AUTH_TOKEN_HEADER = os.getenv("SERVICE_AUTH_TOKEN_HEADER", "Authorization")
SERVICE_AUTH_TOKEN_PREFIX = os.getenv("SERVICE_AUTH_TOKEN_PREFIX", "Bearer ")
SERVICE_AUTH_PROVIDER_HEADER = os.getenv("SERVICE_AUTH_PROVIDER_HEADER", "Authorization-Provider")
SERVICE_AUTH_TOKEN_QUERY = os.getenv("SERVICE_AUTH_TOKEN_QUERY", "authorization")
SERVICE_AUTH_PROVIDER_QUERY = os.getenv("SERVICE_AUTH_PROVIDER_QUERY", "authorization_provider")


class Service(ABC):

    class AuthProvider(Enum):
        UNDEFINED = "undefined"
        FIREBASE = "firebase"

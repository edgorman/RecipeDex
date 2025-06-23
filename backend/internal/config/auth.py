from enum import Enum


AUTHENTICATED_SCOPE = "authenticated"
AUTHORIZATION_HEADER = "Authorization"
AUTHORIZATION_BEARER_PREFIX = "Bearer "
AUTHORIZATION_PROVIDER_HEADER = "Authorization-Provider"


class AuthProvider(Enum):
    FIREBASE = "firebase"

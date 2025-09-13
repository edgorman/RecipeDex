from typing import Any, Dict, Tuple
from google.auth.transport import requests as token_request
from google.oauth2.id_token import verify_firebase_token

from internal.auth.user import UserAuthenticate
from internal.objects.user import User


class FirebaseUserAuthenticate(UserAuthenticate):
    """The FirebaseUserAuthenticate authenticates Users using Firebase."""

    def __init__(self, audience: str) -> None:
        """
        Initialise the FirebaseUserAuthenticate.

        Args:
            audience: the audience of the token.
        """
        self.__audience = audience

    def authenticate(self, provider: User.ProviderType, token: Any) -> Tuple[str, str, Dict[str, Any]]:
        """
        Authenticate a user using a given provider and token.

        Args:
            provider: the provider to authenticate with.
            token: the token to authenticate with.

        Returns:
            a tuple containing the user's ID, name, and the full token info.

        Raises:
            NotImplementedError: if the provider is not supported.
        """
        match provider:
            case User.ProviderType.FIREBASE:
                # Verify the Firebase ID token.
                info = verify_firebase_token(token, token_request.Request(), audience=self.__audience)
                return info["user_id"], info["name"], info
            case _:
                raise NotImplementedError(f"Auth provider `{provider.name}` is not implemented")

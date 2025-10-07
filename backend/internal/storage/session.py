from typing import Any, Dict

from google.adk.sessions import BaseSessionService


class SessionStorage(BaseSessionService):
    """The SessionStorage maintains session information in storage"""

    def update_session_state(self, *, app_name: str, user_id: str, session_id: str, new_state: Dict[str, Any]) -> None:
        """
        Update the state of an existing session.

        Args:
            app_name: the name of the app.
            user_id: the ID of the user.
            session_id: the ID of the session to update.
            new_state: the new state of the session.
        """
        ...

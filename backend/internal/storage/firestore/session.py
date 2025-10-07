import logging
from uuid import uuid4
from typing import Any, Dict, Optional, Tuple
from datetime import datetime, timezone
from google.cloud.firestore import FieldFilter, Client as FirestoreClient
from google.adk.sessions import Session
from google.adk.sessions.base_session_service import GetSessionConfig, ListSessionsResponse
from google.adk.events.event import Event, EventActions

from internal.storage.session import SessionStorage


logger = logging.getLogger(__name__)


class FirestoreSessionStorage(SessionStorage):
    """The FirestoreSessionStorage is an implementation of the SessionStorage that uses Firestore."""

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str]):
        """
        Initialise the FirestoreSessionStorage.

        Args:
            client: the Firestore client.
            collection_path: the path to the collection.
        """
        self.__collection = client.collection(*collection_path)

    async def create_session(
        self,
        *,
        app_name: str,
        user_id: str,
        state: dict = {},
        session_id: str = str(uuid4()),
    ) -> Session:
        """
        Create a new session.

        Args:
            app_name: the name of the app.
            user_id: the ID of the user.
            state: the initial state of the session.
            session_id: the ID of the session.

        Returns:
            the created session.
        """
        try:
            # Create the session object.
            session = Session(
                id=session_id,
                app_name=app_name,
                user_id=user_id,
                state=state,
                events=[],
                last_update_time=datetime.now(tz=timezone.utc).timestamp()
            )

            # Add the session to Firestore.
            # We use a fallback for model_dump because some tools store `builtin_function_or_method` in the events
            self.__collection.add(session.model_dump(mode="json", fallback=str), session_id)

            return session
        except Exception as e:
            detail = f"Could not create session: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

    async def get_session(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        config: Optional[GetSessionConfig] = None,
    ) -> Optional[Session]:
        """
        Get a session by its ID.

        Args:
            app_name: the name of the app.
            user_id: the ID of the user.
            session_id: the ID of the session.
            config: the config for getting the session.

        Returns:
            the session if it exists, otherwise None.
        """
        try:
            # Get the document from Firestore.
            document = self.__collection.document(session_id).get()
        except Exception as e:
            detail = f"Could not get session: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

        # Check the document exists in firestore.
        if not document.exists:
            logger.debug("Could not get session: `document doesn't exist`, returning.")
            return None

        try:
            # Create a session instance from the document.
            session = Session.model_validate(document.to_dict())
        except Exception as e:
            detail = f"Could not format session: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

        return session

    async def append_event(self, session: Session, event: Event) -> Event:
        """
        Append an event to a session.

        Args:
            session: the session to append the event to.
            event: the event to append.

        Returns:
            the appended event.
        """
        updated_event = await super().append_event(session, event)

        try:
            session.last_update_time = event.timestamp
            # Update the session in Firestore.
            # We use a fallback for model_dump because some tools store `builtin_function_or_method` in the events
            self.__collection.document(session.id).set(session.model_dump(mode="json", fallback=str))
        except Exception as e:
            detail = f"Could not update session: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

        return updated_event

    async def list_sessions(self, *, app_name: str, user_id: str) -> ListSessionsResponse:
        """
        List sessions for a user.

        Args:
            app_name: the name of the app.
            user_id: the ID of the user.

        Returns:
            a list of sessions.
        """
        try:
            # Query Firestore for the sessions.
            documents = self.__collection \
                .where(filter=FieldFilter("app_name", "==", app_name)) \
                .where(filter=FieldFilter("user_id", "==", user_id)) \
                .get()

            # Get the documents that exist.
            documents_that_exist = list(filter(lambda document: document.exists, documents))
        except Exception as e:
            detail = f"Could not list sessions: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

        try:
            # Format each session into a session object.
            sessions = [
                Session.model_validate(document.to_dict())
                for document in documents_that_exist
            ]

            return ListSessionsResponse(sessions=sessions)
        except Exception as e:
            detail = f"Could not format sessions: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

    async def delete_session(self, *, app_name: str, user_id: str, session_id: str) -> None:
        """
        Delete a session.

        Args:
            app_name: the name of the app.
            user_id: the ID of the user.
            session_id: the ID of the session to delete.
        """
        try:
            # Delete the session from Firestore.
            self.__collection.document(session_id).delete()
        except Exception as e:
            detail = f"Could not delete session: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

    async def update_session_state(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        new_state: Dict[str, Any]
    ) -> None:
        """
        Update the state of an existing session.

        Args:
            app_name: the name of the app.
            user_id: the ID of the user.
            session_id: the ID of the session to update.
            new_state: the new state of the session.
        """
        # Get the existing session from Firestore.
        session = await self.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
        if session is None:
            e = Exception(f"{session_id} does not exist")
            detail = f"Could not update session state: `{str(e)}`."
            logger.error(detail, exc_info=e)
            raise Exception(detail)

        state_delta = {}

        # Check for changed and new keys
        for new_key, new_value in new_state.items():
            if new_key not in session.state or session.state.get(new_key) != new_value:
                state_delta[new_key] = new_value

        # If there is no diff, return early
        if not state_delta:
            logger.debug("Could not update session state: `no delta generated`, returning.", exc_info=e)
            return

        # Compose a new event to update the state
        actions = EventActions(state_delta=state_delta)
        event = Event(
            invocation_id="create_message_prehook",
            author="system",
            actions=actions
        )

        # Update the state with the event
        await self.append_event(session, event)

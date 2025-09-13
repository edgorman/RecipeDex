from uuid import uuid4
from typing import Optional, Tuple
from datetime import datetime, timezone
from google.cloud.firestore import FieldFilter, Client as FirestoreClient
from google.adk.sessions import Session
from google.adk.sessions.base_session_service import GetSessionConfig, ListSessionsResponse
from google.adk.events.event import Event

from internal.storage.session import SessionStorage


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
            self.__collection.add(session.model_dump(), session_id)

            return session
        except Exception as e:
            raise Exception(f"Could not create session: `{str(e)}`.")

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
            raise Exception(f"Could not get session: `{str(e)}`.")

        if not document.exists:
            return None

        session = Session.model_validate(document.to_dict())

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
            # Update the session in Firestore.
            session.last_update_time = event.timestamp
            self.__collection.document(session.id).set(session.model_dump())
        except Exception as e:
            raise Exception(f"Could not update session after event: `{str(e)}`.")

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
            results = self.__collection \
                .where(filter=FieldFilter("app_name", "==", app_name)) \
                .where(filter=FieldFilter("user_id", "==", user_id)) \
                .get()

            sessions = []
            for document in results:
                if document.exists:
                    sessions.append(Session.model_validate(document.to_dict()))

            return ListSessionsResponse(sessions=sessions)
        except Exception as e:
            raise Exception(f"Could not list sessions: `{str(e)}`.")

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
            raise Exception(f"Could not delete session: `{str(e)}`.")

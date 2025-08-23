from typing import Optional, Tuple
from datetime import datetime, timezone
from google.cloud.firestore import FieldFilter, Client as FirestoreClient
from google.adk.sessions import Session
from google.adk.sessions.base_session_service import GetSessionConfig, ListSessionsResponse
from google.adk.events.event import Event

from internal.storage.session import SessionStorage


class FirestoreSessionStorage(SessionStorage):

    def __init__(self, client: FirestoreClient, collection_path: Tuple[str]):
        self.__collection = client.collection(*collection_path)

    async def create_session(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        state: dict = {},
    ) -> Session:
        try:
            session = Session(
                id=session_id,
                app_name=app_name,
                user_id=user_id,
                state=state,
                events=[],
                last_update_time=datetime.now(tz=timezone.utc).timestamp()
            )

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
        try:
            document = self.__collection.document(session_id).get()
        except Exception as e:
            raise Exception(f"Could not get session: `{str(e)}`.")

        if not document.exists:
            return None

        session = Session(**document.to_dict())

        return session

    async def append_event(self, session: Session, event: Event) -> Event:
        updated_event = await super().append_event(session, event)

        try:
            session.last_update_time = event.timestamp
            self.__collection.document(session.id).set(session.model_dump())
        except Exception as e:
            raise Exception(f"Could not update session after event: `{str(e)}`.")

        return updated_event

    async def list_sessions(self, *, app_name: str, user_id: str) -> ListSessionsResponse:
        try:
            results = self.__collection \
                .where(filter=FieldFilter("app_name", "==", app_name)) \
                .where(filter=FieldFilter("user_id", "==", user_id)) \
                .get()

            sessions = []
            for document in results:
                if document.exists:
                    sessions.append(
                        Session(
                            **document.to_dict()
                        )
                    )

            return ListSessionsResponse(sessions=sessions)
        except Exception as e:
            raise Exception(f"Could not list sessions: `{str(e)}`.")

    async def delete_session(self, *, app_name: str, user_id: str, session_id: str) -> None:
        try:
            self.__collection.document(session_id).delete()
        except Exception as e:
            raise Exception(f"Could not delete session: `{str(e)}`.")

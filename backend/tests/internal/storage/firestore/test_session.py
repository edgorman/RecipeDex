from uuid import uuid4
from unittest.mock import Mock, patch
from datetime import datetime, timezone
import pytest
from google.cloud.firestore_v1 import DocumentSnapshot, DocumentReference
from google.cloud.firestore_v1.query_results import QueryResultsList
from google.adk.sessions import Session
from google.adk.sessions.base_session_service import ListSessionsResponse

from internal.storage.firestore.session import FirestoreSessionStorage


example_session = Session(
    id=str(uuid4()),
    app_name="test_app",
    user_id="test_user",
    state={"key": "value"},
    events=[],
    last_update_time=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).timestamp()
)


@pytest.fixture
def mock_firestore_collection():
    return Mock()


@pytest.fixture
def mock_firestore_client(mock_firestore_collection):
    client = Mock()
    client.collection.return_value = mock_firestore_collection
    return client


@pytest.fixture
def mock_collection_path():
    return ("session",)


def test_init(mock_firestore_client, mock_collection_path):
    _ = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
    mock_firestore_client.collection.assert_called_once_with(*mock_collection_path)


@pytest.mark.asyncio
async def test_create_session(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection
):
    mock_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with patch('internal.storage.firestore.session.datetime') as mock_datetime_module:
        mock_datetime_module.now.return_value = mock_datetime

        client = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
        _ = await client.create_session(
            app_name=example_session.app_name,
            user_id=example_session.user_id,
            session_id=example_session.id,
            state=example_session.state
        )

        mock_firestore_collection.add.assert_called_once_with(example_session.model_dump(), example_session.id)


@pytest.mark.parametrize(
    "session_id,mock_session,expect_session",
    [
        # Session id does exist, session result
        (
            example_session.id, example_session, example_session
        ),
        # Session id does not exist, none result
        (
            str(uuid4()), None, None
        )
    ]
)
@pytest.mark.asyncio
async def test_get_session(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection,
    session_id,
    mock_session,
    expect_session
):
    mock_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with patch('internal.storage.firestore.session.datetime') as mock_datetime_module:
        mock_datetime_module.now.return_value = mock_datetime

        mock_firestore_collection.document.return_value.get.return_value = DocumentSnapshot(
            reference=DocumentReference("session", session_id),
            data=mock_session.model_dump() if mock_session else None,
            exists=mock_session is not None,
            read_time=None,
            create_time=None,
            update_time=None
        )

        client = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
        response_session = await client.get_session(
            app_name=example_session.app_name,
            user_id=example_session.user_id,
            session_id=session_id
        )

        mock_firestore_collection.document.assert_called_with(session_id)
        mock_firestore_collection.document.return_value.get.assert_called_once()

        if mock_session is None:
            assert response_session is None
        else:
            assert response_session.id == expect_session.id
            assert response_session.app_name == expect_session.app_name
            assert response_session.user_id == expect_session.user_id


@pytest.mark.asyncio
async def test_append_event(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection
):
    mock_timestamp = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).timestamp()
    mock_event = Mock()
    mock_event.timestamp = mock_timestamp

    with patch('internal.storage.firestore.session.datetime') as mock_datetime_module:
        mock_datetime_module.now.return_value.timestamp.return_value = mock_timestamp

        client = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
        result_event = await client.append_event(example_session, mock_event)

        assert example_session.last_update_time == mock_timestamp
        mock_firestore_collection.document.assert_called_once_with(example_session.id)
        mock_firestore_collection.document.return_value.set.assert_called_once_with(
            example_session.model_dump()
        )

        assert result_event == mock_event


@pytest.mark.asyncio
async def test_list_sessions(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection
):
    session1 = example_session.model_copy()
    session1.id = str(uuid4())
    session2 = example_session.model_copy()
    session2.id = str(uuid4())

    documents = QueryResultsList([
        DocumentSnapshot(
            reference=DocumentReference("sessions", session1.id),
            data=session1.model_dump(),
            exists=True,
            read_time=None,
            create_time=None,
            update_time=None
        ),
        DocumentSnapshot(
            reference=DocumentReference("sessions", session2.id),
            data=session2.model_dump(),
            exists=True,
            read_time=None,
            create_time=None,
            update_time=None
        )
    ])

    mock_firestore_collection.where.return_value.where.return_value.get.return_value = documents

    client = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
    result = await client.list_sessions(app_name=example_session.app_name, user_id=example_session.user_id)

    mock_firestore_collection.where.assert_called_once()
    call_args = mock_firestore_collection.where.call_args
    filter_arg = call_args.kwargs['filter']
    assert filter_arg.field_path == "app_name"
    assert filter_arg.op_string == "=="
    assert filter_arg.value is example_session.app_name

    mock_firestore_collection.where.return_value.where.assert_called_once()
    call_args = mock_firestore_collection.where.return_value.where.call_args
    filter_arg = call_args.kwargs['filter']
    assert filter_arg.field_path == "user_id"
    assert filter_arg.op_string == "=="
    assert filter_arg.value is example_session.user_id

    assert isinstance(result, ListSessionsResponse)
    assert len(result.sessions) == 2


@pytest.mark.asyncio
async def test_list_sessions_skips_nonexistent_documents(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection
):
    existing_session = Session(
        id=str(uuid4()),
        app_name="test_app",
        user_id="test_user",
        state={},
        last_update_time=datetime.now(tz=timezone.utc).timestamp()
    )

    documents = QueryResultsList([
        DocumentSnapshot(
            reference=DocumentReference("sessions", "test1"),
            data=existing_session.model_dump(),
            exists=True,
            read_time=None,
            create_time=None,
            update_time=None
        ),
        DocumentSnapshot(
            reference=DocumentReference("sessions", "test2"),
            data=None,
            exists=False,
            read_time=None,
            create_time=None,
            update_time=None
        ),
    ])

    mock_firestore_collection.where.return_value.where.return_value.get.return_value = documents

    client = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
    result = await client.list_sessions(app_name="test_app", user_id="test_user")

    assert isinstance(result, ListSessionsResponse)
    assert len(result.sessions) == 1
    assert result.sessions[0].id == existing_session.id


@pytest.mark.asyncio
async def test_delete_session(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection
):
    client = FirestoreSessionStorage(mock_firestore_client, mock_collection_path)
    await client.delete_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session_id"
    )

    mock_firestore_collection.document.assert_called_once_with("test_session_id")
    mock_firestore_collection.document.return_value.delete.assert_called_once()

from uuid import uuid4
from unittest.mock import Mock
import pytest
from google.cloud.firestore_v1 import DocumentSnapshot, DocumentReference
from google.cloud.firestore_v1.query_results import QueryResultsList

from internal.config.auth import AuthProvider
from internal.objects.user import User
from internal.storage.firestore.user import FirestoreUserStorage


example_user = User(
    id=uuid4(),
    name="mock_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=AuthProvider.UNDEFINED,
        info={}
    )
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
    return ("mock", "collection", "path")


def test_init(mock_firestore_client, mock_collection_path):
    _ = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    mock_firestore_client.collection.assert_called_once_with(mock_collection_path)


@pytest.mark.parametrize(
    "user_id,mock_user,expect_user",
    [
        # User id does exist, user result
        (
            example_user.id, example_user, example_user
        ),
        # User id does not exist, none result
        (
            uuid4(), None, None
        )
    ]
)
def test_get(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection,
    user_id,
    mock_user,
    expect_user
):
    # use user id if exists, else random uuid
    mock_firestore_collection.document.return_value.get.return_value = DocumentSnapshot(
        reference=DocumentReference("a", "b"),
        data=mock_user.to_dict() if mock_user else None,
        exists=mock_user is not None,
        read_time=None,
        create_time=None,
        update_time=None
    )

    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    response_user = client.get(user_id)

    mock_firestore_collection.document.assert_called_once_with(str(user_id))
    mock_firestore_collection.document.return_value.get.assert_called_once()

    if mock_user is None:
        assert response_user is None
    else:
        assert response_user.to_dict() == expect_user.to_dict()


@pytest.mark.parametrize(
    "provider_type,provider_id,mock_users,expect_user",
    [
        (
            AuthProvider.UNDEFINED, "provider_id", [example_user], example_user
        ),
        (
            AuthProvider.UNDEFINED, "provider_id", [], None
        )
    ]
)
def test_get_by_provider_id(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection,
    provider_type,
    provider_id,
    mock_users,
    expect_user
):
    # use user id if exists, else random uuid
    mock_firestore_collection.where.return_value.where.return_value.get.return_value = QueryResultsList([
        DocumentSnapshot(
            reference=DocumentReference("a", "b"),
            data=mock_user.to_dict() if mock_user else None,
            exists=mock_user is not None,
            read_time=None,
            create_time=None,
            update_time=None
        )
        for mock_user in mock_users
    ])

    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    response_user = client.get_by_provider_id(provider_id, provider_type)

    mock_firestore_collection.where.assert_called_once_with("provider.type", "==", provider_type.value)
    mock_firestore_collection.where.return_value.where.assert_called_once_with("provider.id", "==", provider_id)
    mock_firestore_collection.where.return_value.where.return_value.get.assert_called_once()

    if len(mock_users) != 1:
        assert response_user is None
    else:
        assert response_user.to_dict() == expect_user.to_dict()


def test_create(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    client.create(example_user)

    mock_firestore_collection.add.assert_called_once_with(example_user.to_dict(), example_user.display_id)


def test_update(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    kwargs = example_user.to_dict()
    kwargs_without_id = kwargs.copy()
    del kwargs_without_id["id"]

    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    client.update(example_user.id, **kwargs)

    mock_firestore_collection.document.assert_called_once_with(example_user.display_id)
    mock_firestore_collection.document.return_value.update.assert_called_once_with(**kwargs_without_id)


def test_delete(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    client.delete(example_user.id)

    mock_firestore_collection.document.assert_called_once_with(example_user.display_id)
    mock_firestore_collection.document.return_value.delete.assert_called_once()

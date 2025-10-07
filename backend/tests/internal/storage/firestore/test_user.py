from uuid import uuid4
from unittest.mock import Mock, patch
from datetime import datetime, timezone
import pytest
from google.cloud.firestore_v1 import DocumentSnapshot, DocumentReference
from google.cloud.firestore_v1.types import StructuredQuery
from google.cloud.firestore_v1.query_results import QueryResultsList

from internal.objects.user import User
from internal.storage.firestore.user import FirestoreUserStorage


example_user = User(
    id=uuid4(),
    name="mock_name",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
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
    mock_firestore_client.collection.assert_called_once_with(*mock_collection_path)


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
        data=mock_user.model_dump(mode="json") if mock_user else None,
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
        assert response_user.model_dump(mode="json") == expect_user.model_dump(mode="json")


@pytest.mark.parametrize(
    "provider_type,provider_id,mock_users,expect_user",
    [
        (
            User.ProviderType.UNDEFINED, "provider_id", [example_user], example_user
        ),
        (
            User.ProviderType.UNDEFINED, "provider_id", [], None
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
    mock_firestore_collection.where.return_value.where.return_value.where.return_value.get.return_value = \
        QueryResultsList([
            DocumentSnapshot(
                reference=DocumentReference("a", "b"),
                data=mock_user.model_dump(mode="json") if mock_user else None,
                exists=mock_user is not None,
                read_time=None,
                create_time=None,
                update_time=None
            )
            for mock_user in mock_users
        ])

    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    response_user = client.get_by_provider_id(provider_id, provider_type)

    mock_firestore_collection.where.assert_called_once()
    call_args = mock_firestore_collection.where.call_args
    filter_arg = call_args.kwargs['filter']
    assert filter_arg.field_path == "deleted_at"
    assert filter_arg.op_string == StructuredQuery.UnaryFilter.Operator.IS_NULL
    assert filter_arg.value is None

    mock_firestore_collection.where.return_value.where.assert_called_once()
    call_args = mock_firestore_collection.where.return_value.where.call_args
    field_arg = call_args.kwargs['filter']
    assert field_arg.field_path == "provider.type"
    assert field_arg.op_string == "=="
    assert field_arg.value == provider_type.value

    mock_firestore_collection.where.return_value.where.return_value.where.assert_called_once()
    call_args = mock_firestore_collection.where.return_value.where.return_value.where.call_args
    field_arg = call_args.kwargs['filter']
    assert field_arg.field_path == "provider.id"
    assert field_arg.op_string == "=="
    assert field_arg.value == provider_id

    mock_firestore_collection.where.return_value.where.return_value.where.return_value.get.assert_called_once()

    if len(mock_users) != 1:
        assert response_user is None
    else:
        assert response_user.model_dump(mode="json") == expect_user.model_dump(mode="json")


def test_create(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
    client.create(example_user)

    mock_firestore_collection.add.assert_called_once_with(
        example_user.model_dump(mode="json"), example_user.display_id
    )


def test_update(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    mock_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with patch('internal.storage.firestore.user.datetime') as mock_datetime_module:
        mock_datetime_module.now.return_value = mock_datetime
        mock_datetime_module.timezone = timezone

        client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
        client.update(example_user.id, example_user)

        expect_user_dict = example_user.model_dump(mode="json")
        expect_user_dict["updated_at"] = mock_datetime.isoformat().replace('+00:00', 'Z')
        mock_firestore_collection.document.assert_called_once_with(str(example_user.id))
        mock_firestore_collection.document.return_value.set.assert_called_once_with(expect_user_dict)


def test_delete(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    mock_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with patch('internal.storage.firestore.user.datetime') as mock_datetime_module:
        mock_datetime_module.now.return_value = mock_datetime
        mock_datetime_module.timezone = timezone

        client = FirestoreUserStorage(mock_firestore_client, mock_collection_path)
        client.delete(example_user.id)

        mock_firestore_collection.document.assert_called_once_with(str(example_user.id))
        mock_firestore_collection.document.return_value.update.assert_called_once_with({"deleted_at": mock_datetime})

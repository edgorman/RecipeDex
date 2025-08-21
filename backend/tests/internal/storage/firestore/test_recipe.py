from uuid import uuid4
from unittest.mock import Mock
import pytest
from google.cloud.firestore_v1 import DocumentSnapshot, DocumentReference
from google.cloud.firestore_v1.query_results import QueryResultsList

from internal.objects.recipe import Recipe
from internal.storage.firestore.recipe import FirestoreRecipeStorage


example_recipe = Recipe(
    id=uuid4(),
    name="mock_recipe",
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
    _ = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    mock_firestore_client.collection.assert_called_once_with(*mock_collection_path)


@pytest.mark.parametrize(
    "recipe_id,mock_recipe,expect_recipe",
    [
        # Recipe id does exist, recipe result
        (
            example_recipe.id, example_recipe, example_recipe
        ),
        # Recipe id does not exist, none result
        (
            uuid4(), None, None
        )
    ]
)
def test_get(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection,
    recipe_id,
    mock_recipe,
    expect_recipe
):
    mock_firestore_collection.document.return_value.get.return_value = DocumentSnapshot(
        reference=DocumentReference("a", "b"),
        data=mock_recipe.to_dict() if mock_recipe else None,
        exists=mock_recipe is not None,
        read_time=None,
        create_time=None,
        update_time=None
    )

    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    response_recipe = client.get(recipe_id)

    mock_firestore_collection.document.assert_called_once_with(str(recipe_id))
    mock_firestore_collection.document.return_value.get.assert_called_once()

    if mock_recipe is None:
        assert response_recipe is None
    else:
        assert response_recipe.to_dict() == expect_recipe.to_dict()


@pytest.mark.parametrize(
    "page,page_size,recipes,expected_len",
    [
        (0, 2, [
            Recipe(id=uuid4(), name="r1"),
            Recipe(id=uuid4(), name="r2"),
            Recipe(id=uuid4(), name="r3"),
        ], 2),
        (1, 2, [
            Recipe(id=uuid4(), name="r1"),
            Recipe(id=uuid4(), name="r2"),
            Recipe(id=uuid4(), name="r3"),
            Recipe(id=uuid4(), name="r4"),
        ], 2),
    ]
)
def test_list_paginates_and_filters_deleted(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection,
    page,
    page_size,
    recipes,
    expected_len,
):
    documents = QueryResultsList([
        DocumentSnapshot(
            reference=DocumentReference("a", "b"),
            data=r.to_dict(),
            exists=True,
            read_time=None,
            create_time=None,
            update_time=None
        )
        for r in recipes
    ])

    mock_firestore_collection.where.return_value \
        .order_by.return_value \
        .offset.return_value \
        .limit.return_value \
        .get.return_value = documents

    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    result = client.list(page=page, page_size=page_size)

    mock_firestore_collection.where.assert_called_once()
    call_args = mock_firestore_collection.where.call_args
    filter_arg = call_args.kwargs['filter']
    assert filter_arg.field_path == "deleted"
    assert filter_arg.op_string == "=="
    assert filter_arg.value is False

    mock_firestore_collection.where.return_value.order_by.assert_called_once_with("name")
    mock_firestore_collection.where.return_value.order_by.return_value.offset.assert_called_once_with(page * page_size)

    expected_limit = min(max(1, page_size), 100)
    mock_firestore_collection.where.return_value \
        .order_by.return_value \
        .offset.return_value \
        .limit.assert_called_once_with(expected_limit)
    mock_firestore_collection.where.return_value \
        .order_by.return_value \
        .offset.return_value \
        .limit.return_value \
        .get.assert_called_once()

    assert isinstance(result, list)
    assert len(result) == expected_len

    input_ids = {r.display_id for r in recipes}
    for recipe in result:
        assert recipe.display_id in input_ids


def test_list_skips_nonexistent_documents(
    mock_firestore_client,
    mock_collection_path,
    mock_firestore_collection
):
    existing_recipe = Recipe(id=uuid4(), name="exists")
    documents = QueryResultsList([
        DocumentSnapshot(
            reference=DocumentReference("a", "b"),
            data=existing_recipe.to_dict(),
            exists=True,
            read_time=None,
            create_time=None,
            update_time=None
        ),
        DocumentSnapshot(
            reference=DocumentReference("a", "c"),
            data=None,
            exists=False,
            read_time=None,
            create_time=None,
            update_time=None
        ),
    ])

    mock_firestore_collection.where.return_value \
        .order_by.return_value \
        .offset.return_value \
        .limit.return_value \
        .get.return_value = documents

    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    result = client.list(page=0, page_size=10)

    assert len(result) == 1
    assert result[0].to_dict() == existing_recipe.to_dict()


def test_create(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    client.create(example_recipe)

    mock_firestore_collection.add.assert_called_once_with(
        document_data=example_recipe.to_dict(),
        document_id=example_recipe.display_id,
    )


def test_update_success(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    kwargs = {"name": "updated_recipe_name"}

    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    client.update(example_recipe.id, **kwargs)

    mock_firestore_collection.document.assert_called_once_with(str(example_recipe.id))
    mock_firestore_collection.document.return_value.update.assert_called_once_with(kwargs)


def test_update_raises_error_for_empty_kwargs(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)

    with pytest.raises(ValueError, match="Could not update recipe: `no fields to update`."):
        client.update(example_recipe.id, **{})

    assert not mock_firestore_collection.document.called
    assert not mock_firestore_collection.document.return_value.update.called


def test_update_raises_error_for_forbidden_keys(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    kwargs = {"id": "forbidden_id"}

    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)

    with pytest.raises(ValueError, match="Could not update recipe: `forbidden field\\(s\\) in args:"):
        client.update(example_recipe.id, **kwargs)

    assert not mock_firestore_collection.document.called
    assert not mock_firestore_collection.document.return_value.update.called


def test_delete(mock_firestore_client, mock_collection_path, mock_firestore_collection):
    client = FirestoreRecipeStorage(mock_firestore_client, mock_collection_path)
    client.delete(example_recipe.id)

    mock_firestore_collection.document.assert_called_once_with(str(example_recipe.id))
    mock_firestore_collection.document.return_value.update.assert_called_once_with({"deleted": True})

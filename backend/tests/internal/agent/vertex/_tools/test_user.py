import pytest
from uuid import uuid4
from unittest.mock import Mock

from internal.objects.user import User
from internal.objects.session import Session
from internal.agent.vertex._tools.user import create_get_user_tools


example_user = User(
    id=uuid4(),
    name="example_user",
    role=User.Role.UNDEFINED,
    provider=User.Provider(
        id="mock_provider_id",
        type=User.ProviderType.UNDEFINED,
        info={}
    )
)


@pytest.fixture
def mock_user_storage_handler():
    return Mock()


@pytest.fixture
def mock_tool_context():
    return Mock()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool_index,expected_value,expected_status",
    [
        (0, example_user.name, Session.Message.ToolResponse.Status.SUCCESS),
    ]
)
async def test_get_user_field_tool(
    mock_user_storage_handler,
    mock_tool_context,
    tool_index,
    expected_value,
    expected_status
):
    mock_tool_context.state.get.return_value = example_user.id
    mock_user_storage_handler.get.return_value = example_user

    tool = create_get_user_tools(mock_user_storage_handler)[tool_index]
    response = await tool.run_async(args={}, tool_context=mock_tool_context)
    tool_response = Session.Message.ToolResponse.model_validate(response)
    assert tool_response.status == expected_status, tool_response.message
    assert tool_response.value == expected_value

    mock_user_storage_handler.get.assert_called_once_with(example_user.id)
    mock_user_storage_handler.update.assert_not_called()

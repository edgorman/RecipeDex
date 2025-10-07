from uuid import UUID
from typing import Dict, List
from pydantic import BaseModel
from google.adk.tools import FunctionTool, ToolContext

from internal.storage.user import UserStorage
from internal.objects.session import Session


def create_get_user_tools(user_storage_handler: UserStorage) -> List[FunctionTool]:
    """
    Creates multiple tools used to get a field of a user.

    Args:
        user_storage_handler: The storage handler for users.

    Returns:
        A list of FunctionTool objects for getting user fields.
    """

    def _get_user_field(id_: UUID, field: str) -> Dict[str, str]:
        """
        Gets the field of a user.

        Args:
            id_: The id of the user to get.
            field: The field of the user to get.

        Returns:
            A dict describing the outcome of the tool usage.
            see https://google.github.io/adk-docs/tools/function-tools/#return-type
        """
        tool_name = f"get_user_{field}_tool"

        try:
            user = user_storage_handler.get(id_)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not load user from internal storage: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            value = getattr(user, field)
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not get user field `{field}`: `{str(e)}`."
            ).model_dump(mode="json")

        try:
            if isinstance(value, BaseModel):
                value = value.model_dump(mode="json")
            elif isinstance(value, list):
                value = [v.model_dump(mode="json") if isinstance(v, BaseModel) else v for v in value]
        except Exception as e:
            return Session.Message.ToolResponse(
                name=tool_name,
                status=Session.Message.ToolResponse.Status.ERROR,
                message=f"Could not format value for user `{field}`: `{str(e)}`."
            ).model_dump(mode="json")

        return Session.Message.ToolResponse(
            name=tool_name,
            status=Session.Message.ToolResponse.Status.SUCCESS,
            value=value,
            message=f"User {field} retrieved successfully."
        ).model_dump(mode="json")

    def get_user_name_tool(tool_context: ToolContext) -> Dict[str, str]:
        """
        Gets the name field of the user.

        Args:
            tool_context: The context of the tool usage.

        Returns:
            A dict describing the outcome
        """
        return _get_user_field(tool_context.state.get("user_id"), "name")

    return [FunctionTool(get_user_name_tool)]

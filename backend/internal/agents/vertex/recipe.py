from uuid import UUID
from typing import List
from google.adk.runners import Runner
from google.genai.types import Content, Part

from internal.agents.recipe import RecipeAgent
from internal.objects.user import User


__ROLE = "user"


class VertexRecipeAgent(RecipeAgent):

    def __init__(self, agent_handler: Runner) -> None:
        self.__agent_handler = agent_handler

    async def message(self, user: User, session_id: UUID, message: str) -> List[str]:
        async for event in self.__agent_handler.run_async(
            user_id=user.display_id,
            session_id=str(session_id),
            new_message=Content(role=__ROLE, parts=[Part.from_text(text=message)]),
        ):
            messages = []
            for response in event.content.parts:
                if response and response.text:
                    messages.append(response)

            return messages

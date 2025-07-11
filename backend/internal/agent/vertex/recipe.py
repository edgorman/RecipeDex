from uuid import UUID
from typing import List
from google.adk.runners import Runner
from google.genai.types import Content, Part

from internal.agent.recipe import RecipeAgent
from internal.objects.user import User
from internal.config.agent import Agent


class VertexRecipeAgent(RecipeAgent):
    """The VertexRecipeAgent is an implementation of the RecipeAgent class"""

    def __init__(self, agent_runner_service: Runner) -> None:
        self.__agent_runner_service = agent_runner_service

    async def message(self, user: User, session_id: UUID, message: str) -> List[str]:
        async for event in self.__agent_runner_service.run_async(
            user_id=user.display_id,
            session_id=str(session_id),
            new_message=Content(role=Agent.Role.USER, parts=[Part.from_text(text=message)]),
        ):
            messages = []
            for response in event.content.parts:
                if response and response.text:
                    messages.append(response)

            return messages

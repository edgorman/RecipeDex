from uuid import uuid4
from typing import AsyncGenerator
from google.adk.runners import Runner
from google.genai.types import Content, Part

from internal.agent.recipe import RecipeAgent
from internal.objects.recipe import Recipe
from internal.objects.user import User


class VertexRecipeAgent(RecipeAgent):
    """The VertexRecipeAgent is an implementation of the RecipeAgent class"""

    def __init__(self, app_name: str, agent_runner_service: Runner) -> None:
        self.__app_name = app_name
        self.__agent_runner_service = agent_runner_service

    async def message(self, user: User, recipe: Recipe, message: str) -> AsyncGenerator[str]:
        if recipe.session_id is None:
            recipe.session_id = uuid4()
            self.__agent_runner_service.session_service.create_session(
                app_name=self.__app_name,
                user_id=user.display_id,
                session_id=str(recipe.session_id)
            )

        async for event in self.__agent_runner_service.run_async(
            user_id=user.display_id,
            session_id=recipe.session_id,
            new_message=Content(role=Recipe.Session.Role.USER, parts=[Part.from_text(text=message)]),
        ):
            for response in event.content.parts:
                if response and response.text:
                    yield response.text

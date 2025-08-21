from typing import AsyncGenerator, Optional
from google.adk.runners import Runner
from google.adk.sessions import Session
from google.adk.events import Event
from google.genai.types import Content, Part

from internal.agent.recipe import RecipeAgent
from internal.objects.recipe import Recipe
from internal.objects.user import User
from internal.storage.recipe import RecipeStorage


class VertexRecipeAgent(RecipeAgent):
    """The VertexRecipeAgent is an implementation of the RecipeAgent class"""

    def __init__(self, agent_runner_service: Runner, recipe_storage_handler: RecipeStorage) -> None:
        self.__agent_runner_service = agent_runner_service
        self.__recipe_storage_handler = recipe_storage_handler

    @staticmethod
    def _parse_role(event: Event) -> Recipe.Message.Role:
        return Recipe.Message.Role.USER if event.author == 'user' else Recipe.Message.Role.MODEL

    async def _get_session(self, recipe: Recipe, user: User) -> Optional[Session]:
        if user.id not in recipe.user_session_mapping:
            return None

        return await self.__agent_runner_service.session_service.get_session(
            app_name=self.__agent_runner_service.app_name,
            user_id=user.display_id,
            session_id=recipe.user_session_mapping[user.id]
        )

    async def get_messages(self, recipe: Recipe, user: User) -> AsyncGenerator[Recipe.Message]:
        session = await self._get_session(recipe, user)
        if session is None:
            return

        for event in session.events:
            for part in event.content.parts:
                if part and part.text:
                    yield Recipe.Message(
                        role=self._parse_role(event),
                        value=part.text
                    )

    async def _create_session(self, recipe: Recipe, user: User) -> None:
        session = await self.__agent_runner_service.session_service.create_session(
            app_name=self.__agent_runner_service.app_name,
            user_id=user.display_id,
        )
        recipe.user_session_mapping[user.id] = session.id
        self.__recipe_storage_handler.update(recipe.id, user_session_mapping={user.id: session.id})

    async def create_message(
        self, recipe: Recipe, user: User, message: Recipe.Message
    ) -> AsyncGenerator[Recipe.Message]:
        session = await self._get_session(recipe, user)
        if session is None:
            await self._create_session(recipe, user)

        async for event in self.__agent_runner_service.run_async(
            user_id=user.display_id,
            session_id=recipe.user_session_mapping[user.id],
            new_message=Content(
                role=message.role,
                parts=[Part.from_text(text=message.value)]
            ),
        ):
            for part in event.content.parts:
                if part and part.text:
                    yield Recipe.Message(
                        role=self._parse_role(event),
                        value=part.text
                    )

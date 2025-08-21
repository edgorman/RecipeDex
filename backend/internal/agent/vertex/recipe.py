from typing import AsyncGenerator, List
from google.adk.runners import Runner
from google.adk.sessions import Session
from google.adk.events import Event
from google.genai.types import Content, Part

from internal.agent.recipe import RecipeAgent
from internal.objects.recipe import Recipe
from internal.storage.recipe import RecipeStorage


class VertexRecipeAgent(RecipeAgent):
    """The VertexRecipeAgent is an implementation of the RecipeAgent class"""

    def __init__(self, app_name: str, agent_runner_service: Runner, recipe_storage_handler: RecipeStorage) -> None:
        self.__app_name = app_name
        self.__agent_runner_service = agent_runner_service
        self.__recipe_storage_handler = recipe_storage_handler

    async def _preprocess(self, recipe: Recipe) -> Session:
        if recipe.session_id is None:
            session = await self.__agent_runner_service.session_service.create_session(
                app_name=self.__app_name,
                user_id=str(recipe.owner_id),
            )
            recipe.session_id = session.id
            self.__recipe_storage_handler.update(recipe.id, sessiond_id=session.id)

        return await self.__agent_runner_service.session_service.get_session(
            app_name=self.__app_name,
            user_id=str(recipe.owner_id),
            session_id=recipe.session_id
        )

    @staticmethod
    def _parse_role(event: Event) -> Recipe.Message.Role:
        return Recipe.Message.Role.USER if event.author == 'user' else Recipe.Message.Role.MODEL

    async def get_messages(self, recipe: Recipe) -> AsyncGenerator[Recipe.Message]:
        session = await self._preprocess(recipe)
        events: List[Event] = session.events

        for event in events:
            for part in event.content.parts:
                if part and part.text:
                    yield Recipe.Message(
                        id=event.author,
                        role=self._parse_role(event),
                        value=part.text
                    )

    async def create_message(self, recipe: Recipe, message: Recipe.Message) -> AsyncGenerator[Recipe.Message]:
        session = await self._preprocess(recipe)

        async for event in self.__agent_runner_service.run_async(
            user_id=str(recipe.owner_id),  # TODO: may be able to use message.author_id
            session_id=session.id,
            new_message=Content(
                role=message.author_role,
                parts=[Part.from_text(text=message.value)]
            ),
        ):
            # TODO: check if even is last with `event.is_final_response`
            for part in event.content.parts:
                if part and part.text:
                    yield Recipe.Message(
                        id=event.author,
                        role=self._parse_role(event),
                        value=part.text
                    )

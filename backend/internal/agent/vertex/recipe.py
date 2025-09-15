from typing import AsyncGenerator, Optional
from google.adk.runners import Runner
from google.adk.sessions import Session
from google.adk.events import Event
from google.genai.types import Content, Part

from internal.agent.recipe import RecipeAgent
from internal.objects.recipe import Recipe
from internal.objects.user import User
from internal.objects.session import SessionState
from internal.storage.recipe import RecipeStorage
from internal.storage.session import SessionStorage


class VertexRecipeAgent(RecipeAgent):
    """The VertexRecipeAgent is an implementation of the RecipeAgent class"""

    def __init__(
        self,
        agent_runner_service: Runner,
        session_storage_handler: SessionStorage,
        recipe_storage_handler: RecipeStorage
    ) -> None:
        """
        Initializes the VertexRecipeAgent.

        Args:
            agent_runner_service: The runner service for the agent.
            session_storage_handler: The session service for the agent.
            recipe_storage_handler: The storage handler for recipes.
        """
        self.__agent_runner_service = agent_runner_service
        self.__session_storage_handler = session_storage_handler
        self.__recipe_storage_handler = recipe_storage_handler

    @staticmethod
    def _parse_role(event: Event) -> Recipe.Message.Role:
        """
        Parses the role from an event.

        Args:
            event: The event to parse.

        Returns:
            The role of the message.
        """
        return Recipe.Message.Role.USER if event.author == 'user' else Recipe.Message.Role.MODEL

    async def _get_session(self, recipe: Recipe, user: User) -> Optional[Session]:
        """
        Gets the session for a user and recipe.

        Args:
            recipe: The recipe to get the session for.
            user: The user to get the session for.

        Returns:
            The session if it exists, otherwise None.
        """
        # If the user does not have a session for this recipe, return None
        if user.id not in recipe.user_session_mapping:
            return None

        # Get the session from the agent runner service
        return await self.__session_storage_handler.get_session(
            app_name=self.__agent_runner_service.app_name,
            user_id=user.display_id,
            session_id=recipe.user_session_mapping[user.id]
        )

    async def _create_session(self, recipe: Recipe, user: User) -> None:
        """
        Creates a session for a user and recipe.

        Args:
            recipe: The recipe to create the session for.
            user: The user to create the session for.
        """
        # Create a new session for the user
        session = await self.__session_storage_handler.create_session(
            app_name=self.__agent_runner_service.app_name,
            user_id=user.display_id,
            state=SessionState(
                recipe_id=recipe.id,
                user_id=user.id
            ).model_dump(mode="json")
        )

        # Update the recipe with the new session id
        recipe.user_session_mapping[user.id] = session.id
        self.__recipe_storage_handler.update(recipe.id, recipe)

    async def get_messages(self, recipe: Recipe, user: User) -> AsyncGenerator[Recipe.Message, None]:
        """
        Gets the messages for a recipe and user.

        Args:
            recipe: The recipe to get the messages for.
            user: The user to get the messages for.

        Yields:
            The messages for the recipe and user.
        """
        # Get the session for the user and recipe
        session = await self._get_session(recipe, user)
        if session is None:
            return

        # Yield the messages from the session
        for event in session.events:
            if event.content:
                for part in event.content.parts:
                    if part and part.text:
                        yield Recipe.Message(
                            role=self._parse_role(event),
                            value=part.text
                        )

    async def create_message(
        self, recipe: Recipe, user: User, message: Recipe.Message
    ) -> AsyncGenerator[Recipe.Message, None]:
        """
        Creates a message for a recipe and user.

        Args:
            recipe: The recipe to create the message for.
            user: The user to create the message for.
            message: The message to create.

        Yields:
            The messages from the agent.
        """
        # Get the session for the user and recipe
        session = await self._get_session(recipe, user)
        if session is None:
            await self._create_session(recipe, user)

        # Run the agent and yield the messages
        async for event in self.__agent_runner_service.run_async(
            user_id=user.display_id,
            session_id=recipe.user_session_mapping[user.id],
            new_message=Content(
                role=message.role,
                parts=[Part.from_text(text=message.value)]
            ),
        ):
            # Produces messages from each response
            # TODO: some events won't have contents, maybe useful to store also
            if event.content:
                for part in event.content.parts:
                    if part and part.text:
                        yield Recipe.Message(
                            role=self._parse_role(event),
                            value=part.text
                        )

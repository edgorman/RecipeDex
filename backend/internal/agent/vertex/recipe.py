from datetime import datetime, timezone
from typing import AsyncGenerator, Optional
from google.adk.runners import Runner
from google.adk.sessions import Session as BaseSession
from google.adk.events import Event
from google.genai.types import Content, Part

from internal.agent.recipe import RecipeAgent
from internal.objects.recipe import Recipe
from internal.objects.user import User
from internal.objects.session import Session
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

    async def _parse_messages(self, event: Event) -> AsyncGenerator[Session.Message, None]:
        """
        Parse the messages from an event.

        Args:
            event: The event to parse.

        Returns:
            The messages from the event
        """
        if event.content:
            created_at = datetime.fromtimestamp(event.timestamp, tz=timezone.utc)

            for part in event.content.parts:
                # Handle chat messages
                if part.text:
                    role = Session.Message.Role.USER if event.author == 'user' else Session.Message.Role.MODEL
                    yield Session.Message(role=role, value=part.text, created_at=created_at)

                # Handle tool completions
                if part.function_response:
                    yield Session.Message(
                        role=Session.Message.Role.SYSTEM,
                        tool=Session.Message.ToolResponse.model_validate(part.function_response.response),
                        created_at=created_at
                    )

                # Handle tool calls
                if part.function_call:
                    yield Session.Message(
                        role=Session.Message.Role.SYSTEM,
                        tool=Session.Message.ToolResponse(
                            name=part.function_call.name,
                            status=Session.Message.ToolResponse.Status.PENDING
                        ),
                        created_at=created_at
                    )

    async def _get_session(self, recipe: Recipe, user: User) -> Optional[BaseSession]:
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
            state=Session.State(
                recipe_id=recipe.id,
                user_id=user.id
            ).model_dump(mode="json")
        )

        # Update the recipe with the new session id
        recipe.user_session_mapping[user.id] = session.id
        self.__recipe_storage_handler.update(recipe.id, recipe)

    async def get_messages(self, recipe: Recipe, user: User) -> AsyncGenerator[Session.Message, None]:
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
            async for message in self._parse_messages(event):
                yield message

    async def create_message(
        self, recipe: Recipe, user: User, message: Session.Message
    ) -> AsyncGenerator[Session.Message, None]:
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
            async for message in self._parse_messages(event):
                yield message

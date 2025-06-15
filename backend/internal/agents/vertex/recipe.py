from uuid import UUID
from google.adk.runners import Runner
from google.genai.types import Content, Part

from internal.agents.recipe import RecipeAgent
from internal.config.chat import ChatAuthor
from internal.objects.user import User
from internal.storage.chat import ChatStorage


class VertexRecipeAgent(RecipeAgent):

    def __init__(self, agent_runner: Runner, chat_handler: ChatStorage) -> None:
        self.__agent_runner = agent_runner
        self.__chat_handler = chat_handler

    async def message(self, user: User, session_id: UUID, message: str) -> None:
        self.__chat_handler.create(ChatAuthor.USER, message)

        async for event in self.__agent_runner.run_async(
            user_id=user.id,
            session_id=str(session_id),
            new_message=Content(role=ChatAuthor.USER, parts=[Part.from_text(text=message)]),
        ):
            for response in event.content.parts:
                if response and response.text:
                    self.__chat_handler.create(ChatAuthor.AGENT, response.text)

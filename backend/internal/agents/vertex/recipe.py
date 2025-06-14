from google.adk.agents import LlmAgent

from internal.config.agent import (
    ROOT_NAME, ROOT_MODEL, ROOT_DESCRIPTION, ROOT_PROMPT
)
from internal.agents.recipe import RecipeAgent


class VertexRecipeAgent(RecipeAgent):

    def __init__(self):
        self.__agent = LlmAgent(
            name=ROOT_NAME,
            model=ROOT_MODEL,
            description=ROOT_DESCRIPTION,
            instruction=ROOT_PROMPT,
            output_key=f"{ROOT_NAME}_output",
            tools=[],
        )

    def message(self):
        ...

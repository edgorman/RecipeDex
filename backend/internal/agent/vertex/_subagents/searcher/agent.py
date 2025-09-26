from google.adk.agents import Agent

from internal.config.agent import AGENT_SEARCHER_NAME, AGENT_MODEL_NAME


class SearcherAgent(Agent):
    """The SearcherAgent is the agent responsible for searching recipes."""

    def __init__(self) -> None:
        """
        Initialise the SearcherAgent class.
        """
        super().__init__(
            name=AGENT_SEARCHER_NAME,
            model=AGENT_MODEL_NAME,
            description="Help users search for recipes on the internet.",
            instruction="""
Role: Act as a search assistant for recipes on the internet.

Instructions: Search the internet using the google search tool for relevant recipes.
Only use reputable websites, and only return URLs that contain a single recipe (ignore collections).
""",
        )

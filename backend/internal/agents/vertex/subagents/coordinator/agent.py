from google.adk.agents import Agent

from . import COORDINATOR_NAME, COORDINATOR_MODEL, COORDINATOR_DESCRIPTION
from .prompt import PROMPT


root_agent = Agent(
    name=COORDINATOR_NAME,
    model=COORDINATOR_MODEL,
    description=COORDINATOR_DESCRIPTION,
    instruction=PROMPT,
    output_key=f"{COORDINATOR_NAME}_output",
    tools=[],
)

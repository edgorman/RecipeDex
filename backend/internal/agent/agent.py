from google.adk.agents import LlmAgent

from internal.config.agent import ROOT_NAME, ROOT_MODEL, ROOT_DESCRIPTION, ROOT_PROMPT


root_agent = LlmAgent(
    name=ROOT_NAME,
    model=ROOT_MODEL,
    description=ROOT_DESCRIPTION,
    instruction=ROOT_PROMPT,
    output_key=f"{ROOT_NAME}_output",
    tools=[],
)

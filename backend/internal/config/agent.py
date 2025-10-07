import os


AGENT_APP_NAME = os.getenv("AGENT_APP_NAME", "recipedex")
AGENT_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
AGENT_PROJECT_REGION = os.getenv("GCP_PROJECT_REGION")

AGENT_MODEL_NAME = "gemini-2.0-flash-001"
AGENT_COORDINATOR_NAME = "coordinator_agent"
AGENT_SEARCHER_NAME = "searcher_agent"

import os
from abc import ABC
from enum import Enum


AGENT_ARTIFACT_BUCKET = os.getenv("AGENT_ARTIFACT_BUCKET")
AGENT_MEMORY_ID = os.getenv("AGENT_MEMORY_CORPUS")


class Agent(ABC):

    class ChatRole(Enum):
        UNDEFINED = "undefined"
        MODEL = "model"
        USER = "user"

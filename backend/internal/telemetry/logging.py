from abc import ABC, abstractmethod
from typing import Optional


class LoggingTelemetry(ABC):
    """The LoggingTelemetry initialises logging for this service."""

    @classmethod
    @abstractmethod
    def setup(cls, log_level: str, service_name: str, gcp_project_id: Optional[str] = None) -> None:
        """Setup the logging for this service."""
        ...

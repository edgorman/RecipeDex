from abc import ABC, abstractmethod
from typing import Optional


class TracingTelemetry(ABC):
    """The TracingTelemetry initialises tracing for this service."""

    @classmethod
    @abstractmethod
    def setup(cls, log_level: str, service_name: str, gcp_project_id: Optional[str] = None) -> None:
        """Setup the tracing for this service."""
        ...

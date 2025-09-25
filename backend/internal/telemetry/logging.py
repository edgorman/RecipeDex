from abc import ABC, abstractmethod


class LoggingTelemetry(ABC):
    """The LoggingTelemetry initialises logging for this service."""

    @classmethod
    @abstractmethod
    def setup(cls, log_level: str, service_name: str) -> None:
        """Setup the logging for this service."""
        ...

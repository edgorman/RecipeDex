import logging
from google.cloud.logging import Client as LoggingClient
from google.cloud.logging.handlers import CloudLoggingHandler

from internal.telemetry.logging import LoggingTelemetry


class GCPLoggingTelemetry(LoggingTelemetry):
    """The GCPLoggingTelemetry initialises cloud logging for this service."""

    @classmethod
    def setup(cls, log_level: str, service_name: str) -> None:
        """
        Setup the logging for this service.

        Args:
            log_level: The level of logging to log.
            service_name: The name of the service.
        """
        logging.info("Using cloud logging handler.")
        client = LoggingClient()
        handler = CloudLoggingHandler(client, name=service_name)
        logging.basicConfig(level=log_level, handlers=[handler])

import logging
from typing import Optional
from google.cloud.logging import Client as LoggingClient
from google.cloud.logging.handlers import CloudLoggingHandler

from internal.telemetry.logging import LoggingTelemetry


class GCPLoggingTelemetry(LoggingTelemetry):
    """The GCPLoggingTelemetry initialises cloud logging for this service."""

    @classmethod
    def setup(cls, log_level: str, service_name: str, gcp_project_id: Optional[str] = None) -> None:
        """
        Setup the tracing for this service.

        Args:
            log_level: The level of logging to log.
            service_name: The name of the service.
            gcp_project_id: The GCP project to trace to.
        """
        if not gcp_project_id:
            raise Exception("Could not initialise cloud logging: missing gcp project id.")

        logging.info("Using cloud logging handler.")
        client = LoggingClient(project=gcp_project_id)
        handler = CloudLoggingHandler(client, name=service_name)
        logging.basicConfig(level=log_level, handlers=[handler])

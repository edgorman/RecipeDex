import sys
import logging
from typing import Optional

from internal.telemetry.logging import LoggingTelemetry


class LocalLoggingTelemetry(LoggingTelemetry):
    """The LocalLoggingTelemetry initialises local logging for this service."""

    @classmethod
    def setup(cls, log_level: str, service_name: str, gcp_project_id: Optional[str] = None) -> None:
        """
        Setup the tracing for this service.

        Args:
            log_level: The level of logging to log.
            service_name: The name of the service.
            gcp_project_id: The GCP project to trace to.
        """
        logging.info("Using local logging handler.")
        handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(level=log_level, handlers=[handler])

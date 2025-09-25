import sys
import logging

from internal.telemetry.logging import LoggingTelemetry


class LocalLoggingTelemetry(LoggingTelemetry):
    """The LocalLoggingTelemetry initialises local logging for this service."""

    @classmethod
    def setup(cls, log_level: str, service_name: str) -> None:
        """
        Setup the logging for this service.

        Args:
            log_level: The level of logging to log.
            service_name: The name of the service.
        """
        logging.info("Using local logging handler.")
        handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(level=log_level, handlers=[handler])

import logging
from typing import Optional
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from internal.telemetry.tracing import TracingTelemetry


class GCPTracingTelemetry(TracingTelemetry):
    """The GCPTracingTelemetry initialises tracing for this service."""

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
            raise Exception("Could not initialise cloud tracing: missing gcp project id.")

        logging.info("Using cloud tracing handler.")
        resource = Resource(attributes={SERVICE_NAME: service_name})
        provider = TracerProvider(resource=resource)
        exporter = CloudTraceSpanExporter(project_id=gcp_project_id)
        processor = BatchSpanProcessor(exporter)

        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        LoggingInstrumentor().instrument(set_logging_format=True, log_level=getattr(logging, log_level))

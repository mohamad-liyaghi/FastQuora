from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from core.settings import settings


def _initial_setup() -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "fastapi-quora"})))
    tracer_provider = trace.get_tracer_provider()
    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.JAEGER_HOST,
        agent_port=settings.JAEGER_PORT,
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))


def _setup_logging() -> None:
    LoggingInstrumentor().instrument()


def _setup_fastapi_instrumentation(app) -> None:
    FastAPIInstrumentor().instrument_app(app)


def setup_opentelemetry(app) -> None:
    _initial_setup()
    _setup_logging()
    _setup_fastapi_instrumentation(app)

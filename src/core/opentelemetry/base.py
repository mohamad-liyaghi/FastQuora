from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME


def setup_opentelemetry():
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "fastapi-quora"})))
    tracer_provider = trace.get_tracer_provider()
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

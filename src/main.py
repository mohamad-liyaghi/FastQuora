from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "fastapi-quora"})))
tracer_provider = trace.get_tracer_provider()
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
app: FastAPI = FastAPI(
    title="Fast Quora",
    description="FastApi Quora Project",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc/",
)

FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

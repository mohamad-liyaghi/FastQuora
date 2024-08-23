from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from core.opentelemetry import setup_opentelemetry

app: FastAPI = FastAPI(
    title="Fast Quora",
    description="FastApi Quora Project",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc/",
)

setup_opentelemetry()
FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

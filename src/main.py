from fastapi import FastAPI
from api import router
from core.middlewares import AuthenticationMiddleware, AuthBackend

from core.opentelemetry import setup_opentelemetry

app: FastAPI = FastAPI(
    title="Fast Quora",
    description="FastApi Quora Project",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc/",
)

app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

app.include_router(router)
setup_opentelemetry(app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

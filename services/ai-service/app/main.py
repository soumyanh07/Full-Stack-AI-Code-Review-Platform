from fastapi import FastAPI

from app.api.v1.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "status": "running",
    }
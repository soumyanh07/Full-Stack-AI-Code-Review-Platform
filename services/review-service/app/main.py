from fastapi import FastAPI
from app.models.review import Review
from app.api.v1.routes import router
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)
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
        "service": "Review Service",
        "status": "running",
    }
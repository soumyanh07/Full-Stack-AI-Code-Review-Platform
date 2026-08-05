from fastapi import FastAPI

from app.api.v1.routes import router
from app.core.config import settings
from app.core.logger import configure_logging
from app.middleware.cors import register_cors
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

register_cors(app)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": settings.APP_NAME, "status": "running"}


app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(
    router,
    prefix="/api/v1",
)
from fastapi import FastAPI

from app.api.v1.routes import router
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from app.middleware.cors import register_cors
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register middleware
register_cors(app)
app.add_middleware(RequestIDMiddleware)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Code Review Auth Service",
        "status": "running",
    }

# API routes
app.include_router(
    router,
    prefix="/api/v1",
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router
from app.api.v1.search import router as search_router
from app.api.v1.review import router as review_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Repository API
app.include_router(
    router,
    prefix="/api/v1",
)

# Semantic Search API
app.include_router(
    search_router,
    prefix="/api/v1",
)

# AI Review API
app.include_router(
    review_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "status": "running",
    }
from fastapi import APIRouter

from app.api.v1.repositories import router as repository_router
from app.api.v1.chat import router as chat_router
from app.api.v1.review import router as review_router
from app.api.v1.webhook import router as webhook_router

router = APIRouter()

router.include_router(repository_router)
router.include_router(chat_router)
router.include_router(review_router)
router.include_router(webhook_router)
from fastapi import APIRouter

from app.api.v1.repositories import router as repositories_router
from app.api.v1.webhook import router as webhook_router
from app.api.v1.search import router as search_router
from app.api.v1.review import router as review_router
from app.api.v1.chat import router as chat_router
from app.api.v1.pr_review import router as pr_review_router

router = APIRouter()


router.include_router(
    repositories_router,
)

router.include_router(
    webhook_router,
)

router.include_router(
    search_router,
)

router.include_router(
    review_router,
)

router.include_router(
    chat_router,
)

router.include_router(
    pr_review_router,
)
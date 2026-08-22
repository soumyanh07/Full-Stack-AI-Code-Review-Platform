from __future__ import annotations

from app.core.celery_app import celery_app
from app.services.pr_review_service import PRReviewService


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def review_pull_request(
    self,
    owner: str,
    repository: str,
    pull_number: int,
):
    """
    Celery task for asynchronous AI Pull Request review.

    GitHub webhook
        ↓
    Celery
        ↓
    GitHub PR files
        ↓
    AI review
        ↓
    GitHub PR review + Check Run
    """

    service = PRReviewService()

    # PRReviewService is async because its public API
    # is designed for FastAPI. The actual GitHub/LLM
    # operations are synchronous.
    import asyncio

    return asyncio.run(
        service.review_pull_request(
            owner=owner,
            repository=repository,
            pull_number=pull_number,
        )
    )
from fastapi import APIRouter, HTTPException

from app.schemas.pull_request import PullRequestReviewRequest
from app.services.pr_review_service import PRReviewService


router = APIRouter(
    prefix="/review",
    tags=["Pull Request Review"],
)


pr_review_service = PRReviewService()


@router.post("/pr")
async def review_pull_request(
    request: PullRequestReviewRequest,
):
    """
    Review changed files in a GitHub Pull Request
    and publish the AI review to GitHub.
    """

    try:
        return await pr_review_service.review_pull_request(
            owner=request.owner,
            repository=request.repository,
            pull_number=request.pr_number,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Pull Request review failed: {str(exc)}",
        )
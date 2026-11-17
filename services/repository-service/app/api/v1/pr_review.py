import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.pull_request import PullRequestReviewRequest
from app.services.pr_review_service import PRReviewService
from app.services.repository_service import RepositoryService
from app.security.jwt import get_current_user


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/review", tags=["Pull Request Review"])
pr_review_service = PRReviewService()


@router.post("/pr")
async def review_pull_request(
    request: PullRequestReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registered = RepositoryService(db).get_repository_by_github_identity(
        request.owner,
        request.repository,
        owner_id=current_user.id,
    )

    if registered is None:
        raise HTTPException(status_code=404, detail="Repository not found.")

    try:
        return await pr_review_service.review_pull_request(
            owner=request.owner,
            repository=request.repository,
            pull_number=request.pr_number,
        )
    except Exception:
        logger.exception(
            "Pull request review failed for %s/%s PR #%s",
            request.owner,
            request.repository,
            request.pr_number,
        )
        raise HTTPException(status_code=500, detail="Pull request review failed.")

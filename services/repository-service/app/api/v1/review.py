from fastapi import APIRouter, Depends, HTTPException

from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.review_service import ReviewService
from app.security.jwt import get_current_user


router = APIRouter(
    prefix="/review",
    tags=["AI Review"],
    dependencies=[Depends(get_current_user)],
)

review_service = ReviewService()


@router.post(
    "",
    response_model=ReviewResponse,
)
def review_code(
    request: ReviewRequest,
):
    try:
        return review_service.review(
            code=request.code,
            language=request.language,
            filename=request.filename,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI review failed: {str(exc)}",
        )
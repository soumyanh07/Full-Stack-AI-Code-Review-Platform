from fastapi import APIRouter, HTTPException

from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.review_service import ReviewService


router = APIRouter(
    prefix="/review",
    tags=["AI Review"],
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
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI review failed: {str(exc)}",
        )
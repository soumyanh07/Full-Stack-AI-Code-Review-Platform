from fastapi import APIRouter

from app.schemas.review import ReviewRequest
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/review",
    tags=["AI Review"],
)

service = ReviewService()


@router.post("")
def review(request: ReviewRequest):
    return service.review(
        request.query,
        request.limit,
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService

router = APIRouter()


@router.post(
    "/reviews",
    response_model=ReviewResponse,
    status_code=201,
)
def create_review(
    request: ReviewCreate,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    return service.review_code(request)
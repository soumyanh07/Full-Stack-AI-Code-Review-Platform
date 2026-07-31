import requests

from app.core.config import settings
from app.repositories.review_repository import ReviewRepository


class ReviewService:

    def __init__(self, db):
        self.repository = ReviewRepository(db)

    def review_code(self, request):
        response = requests.post(
            f"{settings.AI_SERVICE}/api/v1/analyze",
            json={
                "code": request.code
            },
            timeout=120,
        )

        response.raise_for_status()

        ai_review = response.json()["review"]

        review = self.repository.create_review(
            repository_id=request.repository_id,
            review=ai_review,
        )

        return review
from app.clients.ai_client import AIClient
from app.repositories.review_repository import ReviewRepository


class ReviewService:

    def __init__(self, db):
        self.repository = ReviewRepository(db)
        self.ai_client = AIClient()

    def review_code(self, request):
        review = self.ai_client.analyze(request.code)

        return self.repository.create_review(
            repository_id=request.repository_id,
            review=review,
        )
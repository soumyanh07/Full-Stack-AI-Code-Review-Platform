from sqlalchemy.orm import Session

from app.models.review import Review


class ReviewRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_review(self, repository_id: int, review: str):
        new_review = Review(
            repository_id=repository_id,
            review=review,
        )

        self.db.add(new_review)
        self.db.commit()
        self.db.refresh(new_review)

        return new_review
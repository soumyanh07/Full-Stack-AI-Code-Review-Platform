from sqlalchemy.orm import Session

from app.models.repository import Repository


class RepositoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_repository(
        self,
        name: str,
        url: str,
    ) -> Repository:
        repository = Repository(
            name=name,
            url=url,
        )

        self.db.add(repository)
        self.db.commit()
        self.db.refresh(repository)

        return repository

    def get_all(self):
        return self.db.query(Repository).all()

    def get_by_id(self, repo_id: int):
        return (
            self.db.query(Repository)
            .filter(Repository.id == repo_id)
            .first()
        )

    def get_by_url(self, url: str):
        return (
            self.db.query(Repository)
            .filter(Repository.url == url)
            .first()
        )

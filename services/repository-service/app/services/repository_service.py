from __future__ import annotations

import os

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate


class RepositoryService:
    """
    Handles CRUD operations for repositories.
    """

    REPOSITORY_ROOT = "./repositories"

    def __init__(self, db: Session):
        self.db = db

    def get_repositories(self):
        """
        Return all repositories.
        """
        return (
            self.db.query(Repository)
            .order_by(Repository.id.desc())
            .all()
        )

    def get_repository(
        self,
        repo_id: int,
    ):
        """
        Return a single repository.
        """
        repository = (
            self.db.query(Repository)
            .filter(Repository.id == repo_id)
            .first()
        )

        if repository is None:
            raise ValueError("Repository not found.")

        return repository

    def create_repository(
        self,
        repository: RepositoryCreate,
    ):
        """
        Create a new repository.
        """

        existing = (
            self.db.query(Repository)
            .filter(Repository.url == repository.url)
            .first()
        )

        if existing:
            return existing

        os.makedirs(
            self.REPOSITORY_ROOT,
            exist_ok=True,
        )

        local_path = os.path.join(
            self.REPOSITORY_ROOT,
            repository.name,
        )

        db_repository = Repository(
            name=repository.name,
            url=repository.url,
            local_path=local_path,
        )

        self.db.add(db_repository)
        self.db.commit()
        self.db.refresh(db_repository)

        return db_repository
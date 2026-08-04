from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate

from app.services.github_service import GitHubService
from app.services.indexer_service import IndexerService


class RepositoryService:

    def __init__(self, db: Session):
        self.db = db
        self.github = GitHubService()
        self.indexer = IndexerService()

    def create_repository(
        self,
        repository: RepositoryCreate,
    ):
        # Clone repository
        local_path = self.github.clone_repository(
            repository.url
        )

        # Save repository
        db_repo = Repository(
            name=repository.name,
            url=repository.url,
            local_path=local_path,
        )

        self.db.add(db_repo)
        self.db.commit()
        self.db.refresh(db_repo)

        # Automatically index the repository
        self.indexer.index_repository(
            repository_id=db_repo.id,
            repository_path=local_path,
        )

        return db_repo

    def get_repository(self, repo_id: int):
        return (
            self.db.query(Repository)
            .filter(Repository.id == repo_id)
            .first()
        )

    def get_repositories(self):
        return self.db.query(Repository).all()
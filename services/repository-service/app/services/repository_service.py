from fastapi import HTTPException

from app.repositories.repository_repository import RepositoryRepository
from app.services.file_service import FileService
from app.services.github_service import GitHubService
from app.services.indexing_service import IndexingService


class RepositoryService:

    def __init__(self, db):
        self.repository = RepositoryRepository(db)
        self.github = GitHubService()
        self.file_service = FileService()
        self.indexing = IndexingService(db)

    def create_repository(self, repository):

        existing = self.repository.get_by_url(repository.url)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Repository already exists.",
            )

        # Clone GitHub repository
        local_path = self.github.clone_repository(repository.url)

        # Save repository in PostgreSQL
        repo = self.repository.create_repository(
            name=repository.name,
            url=repository.url,
            local_path=local_path,
        )

        # Scan repository files
        files = self.file_service.scan_repository(local_path)

        # Index all files into PostgreSQL
        indexed = self.indexing.index_repository(
            repo.id,
            files,
        )

        print("=" * 60)
        print(f"Repository cloned to: {local_path}")
        print(f"Files found: {len(files)}")
        print(f"Indexed files: {indexed}")
        print("=" * 60)

        return repo

    def get_repositories(self):
        return self.repository.get_all()

    def get_repository(self, repo_id: int):
        return self.repository.get_by_id(repo_id)
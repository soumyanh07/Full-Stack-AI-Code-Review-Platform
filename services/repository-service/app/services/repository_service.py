from fastapi import HTTPException

from app.repositories.repository_repository import RepositoryRepository
from app.repositories.source_file_repository import SourceFileRepository
from app.services.file_service import FileService
from app.services.github_service import GitHubService
from app.services.parser_service import ParserService


class RepositoryService:

    def __init__(self, db):
        self.repository = RepositoryRepository(db)
        self.source_repository = SourceFileRepository(db)
        self.github = GitHubService()
        self.file_service = FileService()
        self.parser = ParserService()

    def create_repository(self, repository):

        existing = self.repository.get_by_url(repository.url)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Repository already exists.",
            )

        local_path = self.github.clone_repository(repository.url)

        repo = self.repository.create_repository(
            name=repository.name,
            url=repository.url,
            local_path=local_path,
        )

        files = self.file_service.scan_repository(local_path)

        print("=" * 60)
        print(f"Repository cloned to: {local_path}")
        print(f"Files found: {len(files)}")

        for file in files:

            parsed = self.parser.parse_file(file)

            self.source_repository.create_file(
                repository_id=repo.id,
                path=parsed["path"],
                language=parsed["language"],
                content=parsed["content"],
            )

            print(parsed["path"])

        print("=" * 60)

        return repo

    def get_repositories(self):
        return self.repository.get_all()

    def get_repository(self, repo_id: int):
        return self.repository.get_by_id(repo_id)
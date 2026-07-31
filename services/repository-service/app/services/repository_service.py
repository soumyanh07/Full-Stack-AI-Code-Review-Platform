from app.repositories.repository_repository import RepositoryRepository


class RepositoryService:

    def __init__(self, db):
        self.repository = RepositoryRepository(db)

    def create_repository(self, repository):
        return self.repository.create_repository(
            name=repository.name,
            url=repository.url,
        )

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, repo_id: int):
        return self.repository.get_by_id(repo_id)

    def get_by_url(self, url: str):
        return self.repository.get_by_url(url)
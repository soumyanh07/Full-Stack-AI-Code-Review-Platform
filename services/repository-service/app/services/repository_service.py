from __future__ import annotations

from app.clients.github_client import GitHubClient


class RepositoryService:
    """
    Business logic for GitHub repositories.
    """

    def __init__(self, token: str):
        self.github = GitHubClient(token)

    async def get_current_user(self):
        return await self.github.get_authenticated_user()

    async def list_repositories(self):
        return await self.github.get_repositories()

    async def get_repository(
        self,
        owner: str,
        repo: str,
    ):
        return await self.github.get_repository(
            owner,
            repo,
        )

    async def list_branches(
        self,
        owner: str,
        repo: str,
    ):
        return await self.github.get_branches(
            owner,
            repo,
        )

    async def list_pull_requests(
        self,
        owner: str,
        repo: str,
    ):
        return await self.github.get_pull_requests(
            owner,
            repo,
        )

    async def list_files(
        self,
        owner: str,
        repo: str,
        path: str = "",
    ):
        return await self.github.get_contents(
            owner,
            repo,
            path,
        )
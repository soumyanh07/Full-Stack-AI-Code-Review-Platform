from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class GitHubClient:
    """
    Production-ready GitHub API client.

    All communication with GitHub should happen through this class.
    """

    def __init__(self, token: str | None = None):
        self.base_url = settings.GITHUB_API
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": settings.APP_NAME,
        }

        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    async def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Any:
        """
        Generic GitHub request.
        """

        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs,
            )

            response.raise_for_status()

            return response.json()

    async def get_authenticated_user(self):
        return await self.request(
            "GET",
            "/user",
        )

    async def get_repositories(self):
        return await self.request(
            "GET",
            "/user/repos",
        )

    async def get_repository(
        self,
        owner: str,
        repo: str,
    ):
        return await self.request(
            "GET",
            f"/repos/{owner}/{repo}",
        )

    async def get_branches(
        self,
        owner: str,
        repo: str,
    ):
        return await self.request(
            "GET",
            f"/repos/{owner}/{repo}/branches",
        )

    async def get_pull_requests(
        self,
        owner: str,
        repo: str,
    ):
        return await self.request(
            "GET",
            f"/repos/{owner}/{repo}/pulls",
        )

    async def get_contents(
        self,
        owner: str,
        repo: str,
        path: str = "",
    ):
        return await self.request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{path}",
        )
from __future__ import annotations

import requests

from app.core.config import settings


class GitHubClient:

    def __init__(self):

        self.base_url = "https://api.github.com"

        self.headers = {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }

    def get_pull_request_files(
        self,
        repository: str,
        pr_number: int,
    ):

        url = (
            f"{self.base_url}/repos/"
            f"{repository}/pulls/{pr_number}/files"
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=60,
        )

        response.raise_for_status()

        return response.json()
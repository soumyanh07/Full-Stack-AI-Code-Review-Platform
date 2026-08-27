from __future__ import annotations

import shutil
from pathlib import Path

from git import Repo, GitCommandError

from app.core.config import settings


class GitHubService:
    """
    Handles cloning and updating Git repositories.
    """

    def __init__(self):
        self.base_path = Path(settings.REPOSITORY_STORAGE)

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def repository_path(
        self,
        owner: str,
        repository: str,
    ) -> Path:
        return self.base_path / owner / repository

    def clone_repository(
        self,
        clone_url: str,
        owner: str,
        repository: str,
    ) -> Path:

        repo_path = self.repository_path(
            owner,
            repository,
        )

        if repo_path.exists():
            return repo_path

        repo_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        Repo.clone_from(
            clone_url,
            repo_path,
        )

        return repo_path

    def pull_repository(
        self,
        owner: str,
        repository: str,
    ) -> Path:

        repo_path = self.repository_path(
            owner,
            repository,
        )

        if not repo_path.exists():
            raise FileNotFoundError(
                "Repository not cloned."
            )

        repo = Repo(repo_path)

        repo.remotes.origin.pull()

        return repo_path

    def delete_repository(
        self,
        owner: str,
        repository: str,
    ):

        repo_path = self.repository_path(
            owner,
            repository,
        )

        if repo_path.exists():
            shutil.rmtree(repo_path)

    def repository_exists(
        self,
        owner: str,
        repository: str,
    ) -> bool:

        return self.repository_path(
            owner,
            repository,
        ).exists()
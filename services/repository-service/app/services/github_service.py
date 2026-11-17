from __future__ import annotations

import shutil
from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from app.core.config import settings


class GitHubService:
    """Clone and update repositories in isolated storage directories."""

    def __init__(self):
        self.base_path = Path(
            settings.REPOSITORY_STORAGE
        ).expanduser().resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _resolve_repository_path(
        self,
        local_path: str,
        repository_id: int,
    ) -> Path:
        expected = self.base_path / str(repository_id)
        supplied = Path(local_path).expanduser()

        if not supplied.is_absolute():
            supplied = supplied.absolute()

        if repository_id <= 0 or supplied != expected:
            raise ValueError(
                "Repository storage path does not match its registered ID."
            )

        if expected.is_symlink():
            raise ValueError(
                "Repository storage path must not be a symbolic link."
            )

        return expected

    @staticmethod
    def _normalize_remote_url(url: str) -> str:
        return url.strip().rstrip("/").removesuffix(".git").casefold()

    def clone_repository(
        self,
        clone_url: str,
        local_path: str,
        repository_id: int,
    ) -> Path:
        repo_path = self._resolve_repository_path(
            local_path,
            repository_id,
        )

        if repo_path.exists():
            try:
                repo = Repo(repo_path)
                origin_url = repo.remotes.origin.url
            except Exception as exc:
                raise RuntimeError(
                    "The registered repository directory is not a valid Git clone."
                ) from exc

            if self._normalize_remote_url(origin_url) != self._normalize_remote_url(
                clone_url
            ):
                raise RuntimeError(
                    "Existing clone remote does not match the registered repository."
                )

            try:
                repo.git.pull("--ff-only")
            except GitCommandError as exc:
                raise RuntimeError(
                    "Could not update the existing repository clone."
                ) from exc

            return repo_path

        repo_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            Repo.clone_from(clone_url, repo_path)
        except Exception:
            if repo_path.exists():
                shutil.rmtree(repo_path)
            raise

        return repo_path

    def pull_repository(
        self,
        local_path: str,
        repository_id: int,
    ) -> Path:
        repo_path = self._resolve_repository_path(local_path, repository_id)

        if not repo_path.is_dir():
            raise FileNotFoundError("Repository not cloned.")

        repo = Repo(repo_path)
        repo.git.pull("--ff-only")
        return repo_path

    def delete_repository(
        self,
        local_path: str,
        repository_id: int,
    ) -> None:
        repo_path = self._resolve_repository_path(local_path, repository_id)

        if repo_path.exists():
            Repo(repo_path)
            shutil.rmtree(repo_path)

    def repository_exists(
        self,
        local_path: str,
        repository_id: int,
    ) -> bool:
        repo_path = self._resolve_repository_path(local_path, repository_id)
        return repo_path.is_dir() and (repo_path / ".git").is_dir()

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

from github import Github

from app.core.config import settings


class GitHubAPIService:
    """
    Service for interacting with GitHub repositories and Pull Requests.
    """

    def __init__(self):
        self.github = Github(settings.GITHUB_TOKEN)

    # ============================================================
    # Repository Operations
    # ============================================================

    def clone_repository(self, repo_url: str) -> str:
        """
        Clone a GitHub repository into a temporary directory.

        Args:
            repo_url: GitHub repository URL.

        Returns:
            Path to the cloned repository.
        """

        temp_dir = tempfile.mkdtemp()

        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    repo_url,
                    temp_dir,
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            return temp_dir

        except Exception:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            raise

    def delete_repository(self, path: str) -> None:
        """
        Delete a cloned repository directory.
        """

        if os.path.exists(path):
            shutil.rmtree(path)

    # ============================================================
    # Pull Request Operations
    # ============================================================

    def get_pull_request_files(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ) -> list[dict]:
        """
        Get files changed by a GitHub Pull Request.

        Args:
            owner: GitHub repository owner.
            repository: Repository name.
            pull_number: Pull Request number.

        Returns:
            List of changed files with filename, status and patch.
        """

        repo = self.github.get_repo(
            f"{owner}/{repository}"
        )

        pull_request = repo.get_pull(
            pull_number
        )

        files = []

        for file in pull_request.get_files():
            files.append(
                {
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch,
                }
            )

        return files
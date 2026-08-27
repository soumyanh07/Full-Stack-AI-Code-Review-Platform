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
        if not settings.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is not configured.")

        self.github = Github(settings.GITHUB_TOKEN)

    # ============================================================
    # Repository Operations
    # ============================================================

    def clone_repository(self, repo_url: str) -> str:
        """
        Clone a GitHub repository into a temporary directory.
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

    def get_pull_request(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ):
        """
        Return a GitHub Pull Request object.
        """

        repo = self.github.get_repo(
            f"{owner}/{repository}"
        )

        return repo.get_pull(
            pull_number
        )

    def get_pull_request_files(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ) -> list[dict]:
        """
        Get files changed by a GitHub Pull Request.
        """

        pull_request = self.get_pull_request(
            owner=owner,
            repository=repository,
            pull_number=pull_number,
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

    # ============================================================
    # Pull Request Review
    # ============================================================

    def create_pull_request_review(
        self,
        owner: str,
        repository: str,
        pull_number: int,
        body: str,
        event: str = "COMMENT",
    ) -> dict:
        """
        Post an AI-generated review to a GitHub Pull Request.

        event can be:
        - COMMENT
        - APPROVE
        - REQUEST_CHANGES
        """

        pull_request = self.get_pull_request(
            owner=owner,
            repository=repository,
            pull_number=pull_number,
        )

        review = pull_request.create_review(
            body=body,
            event=event,
        )

        return {
            "id": review.id,
            "url": review.html_url,
            "state": review.state,
        }

    # ============================================================
    # GitHub Checks
    # ============================================================

    def create_check_run(
        self,
        owner: str,
        repository: str,
        head_sha: str,
        title: str,
        summary: str,
        conclusion: str = "success",
        name: str = "AI Code Review",
    ) -> dict:
        """
        Create a GitHub Check Run for an AI review.
        """

        repo = self.github.get_repo(
            f"{owner}/{repository}"
        )

        check = repo.create_check_run(
            name=name,
            head_sha=head_sha,
            status="completed",
            conclusion=conclusion,
            output={
                "title": title,
                "summary": summary,
            },
        )

        return {
            "id": check.id,
            "url": check.html_url,
            "name": check.name,
            "status": check.status,
            "conclusion": check.conclusion,
        }
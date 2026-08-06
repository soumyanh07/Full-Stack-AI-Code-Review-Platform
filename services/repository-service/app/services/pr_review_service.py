from __future__ import annotations

from app.clients.github_client import GitHubClient
from app.services.review_service import ReviewService


class PRReviewService:
    """
    Reviews every changed file in a Pull Request.
    """

    def __init__(self):
        self.github = GitHubClient()
        self.reviewer = ReviewService()

    def review_pull_request(
        self,
        repository: str,
        pr_number: int,
    ) -> dict:
        """
        Review an entire Pull Request.
        """

        files = self.github.get_pull_request_files(
            repository=repository,
            pr_number=pr_number,
        )

        reviews = []

        for file in files:

            filename = file.get("filename")

            patch = file.get("patch")

            if not patch:
                continue

            result = self.reviewer.review_code(
                code=patch,
                language=self._detect_language(filename),
            )

            reviews.append(
                {
                    "filename": filename,
                    "review": result["review"],
                }
            )

        return {
            "repository": repository,
            "pull_request": pr_number,
            "reviews": reviews,
        }

    def _detect_language(
        self,
        filename: str,
    ) -> str:

        extension = filename.split(".")[-1].lower()

        mapping = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "tsx": "typescript",
            "jsx": "javascript",
            "java": "java",
            "cpp": "cpp",
            "cc": "cpp",
            "c": "c",
            "cs": "csharp",
            "go": "go",
            "rs": "rust",
            "php": "php",
            "rb": "ruby",
            "swift": "swift",
            "kt": "kotlin",
            "scala": "scala",
            "html": "html",
            "css": "css",
            "json": "json",
            "yaml": "yaml",
            "yml": "yaml",
            "sql": "sql",
        }

        return mapping.get(extension, "text")
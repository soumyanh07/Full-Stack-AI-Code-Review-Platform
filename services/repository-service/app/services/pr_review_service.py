from __future__ import annotations

from app.services.github_api_service import GitHubAPIService
from app.services.review_service import ReviewService


class PRReviewService:
    """
    AI-powered Pull Request review service.

    Fetches changed files from GitHub and sends their patches
    through the AI code review pipeline.
    """

    def __init__(self):
        self.github = GitHubAPIService()
        self.review_service = ReviewService()

    async def review_pull_request(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ) -> list[dict]:
        """
        Review all reviewable files changed in a Pull Request.
        """

        files = self.github.get_pull_request_files(
            owner=owner,
            repository=repository,
            pull_number=pull_number,
        )

        results = []

        for file in files:
            filename = file.get(
                "filename",
                "",
            )

            patch = file.get(
                "patch"
            )

            # GitHub does not provide patches for
            # some binary or unsupported files.
            if not patch:
                continue

            language = self._detect_language(
                filename
            )

            result = self.review_service.review(
                code=patch,
                language=language,
                filename=filename,
            )

            results.append(
                result
            )

        return results

    @staticmethod
    def _detect_language(
        filename: str,
    ) -> str:
        """
        Detect programming language from filename extension.
        """

        extension = ""

        if "." in filename:
            extension = (
                filename
                .rsplit(".", 1)[-1]
                .lower()
            )

        mapping = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "tsx": "typescript",
            "jsx": "javascript",
            "java": "java",
            "cpp": "cpp",
            "cc": "cpp",
            "cxx": "cpp",
            "c": "c",
            "h": "c",
            "hpp": "cpp",
            "go": "go",
            "rs": "rust",
            "php": "php",
            "rb": "ruby",
            "sql": "sql",
            "html": "html",
            "css": "css",
            "scss": "scss",
            "json": "json",
            "yaml": "yaml",
            "yml": "yaml",
            "md": "markdown",
        }

        return mapping.get(
            extension,
            "text",
        )
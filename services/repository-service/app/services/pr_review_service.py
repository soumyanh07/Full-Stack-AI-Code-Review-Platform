from __future__ import annotations

from app.services.github_api_service import GitHubAPIService
from app.services.review_service import ReviewService


class PRReviewService:
    """
    Reviews changed files in a GitHub Pull Request.
    """

    def __init__(self):
        self.github = GitHubAPIService()
        self.review = ReviewService()

    async def review_pull_request(
        self,
        owner: str,
        repository: str,
        pull_number: int,
        token: str,
    ) -> list[dict]:

        files = await self.github.get_pull_request_files(
            owner=owner,
            repository=repository,
            pull_number=pull_number,
            token=token,
        )

        results = []

        for file in files:

            filename = file.get(
                "filename",
                ""
            )

            patch = file.get(
                "patch"
            )

            if not patch:
                continue

            language = self._detect_language(
                filename
            )

            result = self.review.review(
                code=patch,
                language=language,
                filename=filename,
            )

            results.append(
                result
            )

        return results

    def _detect_language(
        self,
        filename: str,
    ) -> str:

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
            "c": "c",
            "go": "go",
            "rs": "rust",
            "php": "php",
            "rb": "ruby",
            "sql": "sql",
            "html": "html",
            "css": "css",
        }

        return mapping.get(
            extension,
            "text",
        )
from typing import Dict, List

from app.services.github_client import GitHubClient
from app.services.ai_review_client import AIReviewClient


class PRReviewService:
    """
    Handles complete Pull Request review workflow.
    """

    def __init__(self):
        self.github = GitHubClient()
        self.ai_review = AIReviewClient()


    async def review_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        token: str
    ) -> Dict:


        # 1. Get changed files from GitHub
        changed_files = await self.github.get_pull_request_files(
            owner,
            repo,
            pull_number,
            token
        )


        files = []

        for file in changed_files:

            content = await self.github.get_file_content(
                owner,
                repo,
                file["filename"],
                token
            )

            files.append(
                {
                    "path": file["filename"],
                    "content": content,
                    "language": self.detect_language(
                        file["filename"]
                    )
                }
            )


        # 2. Send code to AI Review Service
        review_result = await self.ai_review.review_repository(
            files
        )


        # 3. Create GitHub review comment
        await self.github.create_review_comment(
            owner,
            repo,
            pull_number,
            review_result,
            token
        )


        return {
            "repository": f"{owner}/{repo}",
            "pull_request": pull_number,
            "status": "completed",
            "review": review_result
        }



    def detect_language(
        self,
        filename: str
    ) -> str:

        extension = filename.split(".")[-1]


        languages = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "java": "java",
            "cpp": "cpp",
            "go": "go",
            "rs": "rust"
        }


        return languages.get(
            extension,
            "unknown"
        )
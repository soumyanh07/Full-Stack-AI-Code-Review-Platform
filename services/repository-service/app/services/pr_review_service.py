from github import Github

from app.core.config import settings
from app.services.review_service import ReviewService


class PRReviewService:

    MAX_PATCH_CHARS = 12000

    def __init__(self):
        self.github = Github(settings.GITHUB_TOKEN)
        self.review = ReviewService()

    def review_pull_request(
        self,
        repository: str,
        pr_number: int,
    ):
        repo = self.github.get_repo(repository)
        pr = repo.get_pull(pr_number)

        reviews = []

        for file in pr.get_files():

            # GitHub does not provide a patch for binary files
            # and some files may have no patch at all.
            if not file.patch:
                continue

            patch = file.patch

            # Prevent very large diffs from overwhelming the LLM.
            truncated = len(patch) > self.MAX_PATCH_CHARS

            if truncated:
                patch = (
                    patch[:self.MAX_PATCH_CHARS]
                    + "\n\n"
                    "[PATCH TRUNCATED: remaining diff omitted]"
                )

            result = self.review.review(patch)

            reviews.append(
                {
                    "file": file.filename,
                    "review": result,
                    "truncated": truncated,
                    "patch_chars": len(patch),
                }
            )

        return reviews
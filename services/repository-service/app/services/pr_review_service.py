from github import Github

from app.core.config import settings

from app.services.review_service import ReviewService


class PRReviewService:

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

            if not file.patch:
                continue

            result = self.review.review(
                file.patch
            )

            reviews.append(
                {
                    "file": file.filename,
                    "review": result,
                }
            )

        return reviews
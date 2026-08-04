from pydantic import BaseModel


class PullRequestReviewRequest(BaseModel):
    repository: str
    pr_number: int
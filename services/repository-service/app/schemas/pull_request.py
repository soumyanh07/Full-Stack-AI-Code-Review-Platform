from pydantic import BaseModel, Field


class PullRequestReviewRequest(BaseModel):
    owner: str = Field(
        min_length=1,
        max_length=100,
    )

    repository: str = Field(
        min_length=1,
        max_length=200,
    )

    pr_number: int = Field(
        gt=0,
    )
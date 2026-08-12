from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=100000,
    )

    language: str = Field(
        default="text",
        min_length=1,
        max_length=50,
    )


class ReviewResponse(BaseModel):
    language: str

    review: str
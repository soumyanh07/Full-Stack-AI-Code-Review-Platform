from pydantic import BaseModel


class ReviewCreate(BaseModel):
    repository_id: int
    code: str


class ReviewResponse(BaseModel):
    id: int
    repository_id: int
    review: str

    class Config:
        from_attributes = True
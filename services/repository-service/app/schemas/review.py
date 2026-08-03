from pydantic import BaseModel


class ReviewRequest(BaseModel):
    query: str
    limit: int = 5
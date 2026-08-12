from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    repository_id: int = Field(
        gt=0
    )

    question: str = Field(
        min_length=1,
        max_length=4000,
    )


class ChatResponse(BaseModel):

    repository_id: int

    question: str

    answer: str

    context: str
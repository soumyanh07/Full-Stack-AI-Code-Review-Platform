from pydantic import BaseModel


class ChatRequest(BaseModel):
    repository_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str
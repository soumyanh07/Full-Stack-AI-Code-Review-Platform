from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    code: str


class AnalyzeResponse(BaseModel):
    review: str
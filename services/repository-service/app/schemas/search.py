from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    repository_id: int
    source_file_id: int
    path: str
    chunk: int
    text: str
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResult]
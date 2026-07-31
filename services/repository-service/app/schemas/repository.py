from pydantic import BaseModel


class RepositoryCreate(BaseModel):
    name: str
    url: str


class RepositoryResponse(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        from_attributes = True
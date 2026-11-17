from pydantic import BaseModel, ConfigDict, Field


class RepositoryCreate(BaseModel):
    name: str | None = None
    url: str = Field(min_length=1, max_length=500)


class RepositoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str

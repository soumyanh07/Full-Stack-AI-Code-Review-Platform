from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository_service import RepositoryService

router = APIRouter()


@router.get("/")
def root():
    return {
        "service": "Repository Service",
        "status": "running",
    }


@router.get(
    "/repositories",
    response_model=list[RepositoryResponse],
)
def get_repositories(
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.get_repositories()


@router.post(
    "/repositories",
    response_model=RepositoryResponse,
    status_code=201,
)
def create_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.create_repository(repository)


@router.get(
    "/repositories/{repo_id}",
    response_model=RepositoryResponse,
)
def get_repository(
    repo_id: int,
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.get_repository(repo_id)
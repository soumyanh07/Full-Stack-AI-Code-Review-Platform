from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.schemas.repository import RepositoryResponse
from app.services.repository_service import RepositoryService


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
async def list_repositories(
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)
    return service.get_repositories()


@router.get(
    "/{repo_id}",
    response_model=RepositoryResponse,
)
async def repository_details(
    repo_id: int,
    db: Session = Depends(get_db),
):
    service = RepositoryService(db)

    try:
        return service.get_repository(repo_id)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Repository not found.",
        )
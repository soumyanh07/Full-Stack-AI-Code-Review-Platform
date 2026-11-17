from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.repository_service import RepositoryService
from app.security.jwt import get_current_user


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_repository(
    request: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repository = RepositoryService(db).create_repository(
            request,
            owner_id=current_user.id,
        )
        return repository
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[RepositoryResponse])
def list_repositories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RepositoryService(db).get_repositories(current_user.id)


@router.get("/{repo_id}", response_model=RepositoryResponse)
def repository_details(
    repo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return RepositoryService(db).get_repository(
            repo_id,
            owner_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Repository not found.") from exc

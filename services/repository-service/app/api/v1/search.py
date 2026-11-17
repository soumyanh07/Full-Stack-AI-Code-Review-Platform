import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.services.repository_service import RepositoryService
from app.services.search_service import SearchService
from app.security.jwt import get_current_user


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["Semantic Search"])


@router.get("/{repository_id}")
def search_repository(
    repository_id: int,
    q: str,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    if limit < 1 or limit > 20:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 20.")

    try:
        RepositoryService(db).get_repository(
            repository_id,
            owner_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Repository not found.") from exc

    try:
        results = SearchService().search(
            repository_id=repository_id,
            query=q,
            limit=limit,
        )
    except Exception:
        logger.exception("Semantic search failed for repository %s", repository_id)
        raise HTTPException(status_code=500, detail="Unable to search this repository.")

    return {
        "repository_id": repository_id,
        "query": q,
        "count": len(results),
        "results": results,
    }

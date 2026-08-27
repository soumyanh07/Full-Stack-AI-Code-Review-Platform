from fastapi import APIRouter, HTTPException

from app.services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"],
)


@router.get("/{repository_id}")
async def search_repository(
    repository_id: int,
    q: str,
    limit: int = 5,
):
    """
    Semantic search inside a repository.
    """

    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    if limit < 1 or limit > 20:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 20.",
        )

    service = SearchService()

    results = service.search(
        repository_id=repository_id,
        query=q,
        limit=limit,
    )

    return {
        "repository_id": repository_id,
        "query": q,
        "count": len(results),
        "results": results,
    }
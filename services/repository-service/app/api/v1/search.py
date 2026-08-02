from fastapi import APIRouter

from app.schemas.search import SearchRequest
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"],
)

service = SearchService()


@router.post("")
def semantic_search(request: SearchRequest):

    results = service.search(
        request.query,
        request.limit,
    )

    response = []

    for result in results:
        response.append(
            {
                "repository_id": result.payload["repository_id"],
                "source_file_id": result.payload["source_file_id"],
                "path": result.payload["path"],
                "chunk": result.payload["chunk"],
                "text": result.payload["text"],
                "score": result.score,
            }
        )

    return {
        "results": response
    }
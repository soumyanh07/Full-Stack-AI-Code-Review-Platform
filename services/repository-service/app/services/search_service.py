from __future__ import annotations

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class SearchService:
    """
    Performs semantic code search using embeddings and Qdrant.
    """

    # Ignore results that are too weakly related to the question.
    MIN_SIMILARITY = 0.55

    def __init__(self):
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()

    def search(
        self,
        repository_id: int,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        if not query.strip():
            return []

        # ---------------------------------------------
        # Step 1: Embed the user's question
        # ---------------------------------------------

        query_vector = self.embedding.embed_query(query)

        # ---------------------------------------------
        # Step 2: Search Qdrant
        # ---------------------------------------------

        results = self.qdrant.search_repository(
            repository_id=repository_id,
            vector=query_vector,
            limit=limit,
        )

        output = []

        # ---------------------------------------------
        # Step 3: Convert Qdrant results
        # ---------------------------------------------

        for result in results:

            payload = result.payload or {}

            score = float(result.score)

            # -----------------------------------------
            # Ignore weak semantic matches
            # -----------------------------------------

            if score < self.MIN_SIMILARITY:
                continue

            output.append(
                {
                    "score": score,
                    "repository_id": payload.get(
                        "repository_id"
                    ),
                    "filename": payload.get(
                        "filename"
                    ),
                    "path": payload.get(
                        "path"
                    ),
                    "language": payload.get(
                        "language"
                    ),
                    "chunk_id": payload.get(
                        "chunk_id"
                    ),
                    "content": payload.get(
                        "content"
                    ),
                }
            )

        return output
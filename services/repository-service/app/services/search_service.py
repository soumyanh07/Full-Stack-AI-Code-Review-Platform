from __future__ import annotations

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class SearchService:
    """
    Performs semantic code search using embeddings and Qdrant.
    """

    MIN_SIMILARITY = 0.55

    EXCLUDED_EXTENSIONS = {
        ".md",
        ".txt",
        ".rst",
    }

    # Maximum number of chunks we allow from the same file.
    # This improves questions that require understanding
    # multiple parts of the same implementation file.
    MAX_CHUNKS_PER_FILE = 1

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
        # Step 1: Embed user question
        # ---------------------------------------------

        query_vector = self.embedding.embed_query(query)

        # ---------------------------------------------
        # Step 2: Retrieve extra candidates
        # ---------------------------------------------

        results = self.qdrant.search_repository(
            repository_id=repository_id,
            vector=query_vector,
            limit=limit * 4,
        )

        output = []

        # Track how many chunks came from each file.
        file_chunk_counts: dict[str, int] = {}

        # ---------------------------------------------
        # Step 3: Filter and deduplicate
        # ---------------------------------------------

        for result in results:

            payload = result.payload or {}

            score = float(result.score)

            # Ignore weak matches.
            if score < self.MIN_SIMILARITY:
                continue

            path = payload.get("path") or ""

            # Ignore documentation files.
            if any(
                path.lower().endswith(extension)
                for extension in self.EXCLUDED_EXTENSIONS
            ):
                continue

            normalized_path = path.lower()

            current_count = file_chunk_counts.get(
                normalized_path,
                0,
            )

            # Allow up to two useful chunks from the same
            # implementation file.
            if current_count >= 1:
                continue

            file_chunk_counts[normalized_path] = (
                current_count + 1
            )

            output.append(
                {
                    "score": score,
                    "repository_id": payload.get(
                        "repository_id"
                    ),
                    "filename": payload.get(
                        "filename"
                    ),
                    "path": path,
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

            if len(output) >= limit:
                break

        return output
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class SearchService:

    def __init__(self):
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()

    def search(self, query: str, limit: int = 5):

        embedding = self.embedding.generate_embedding(query)

        results = self.qdrant.search(
            embedding=embedding,
            limit=limit,
        )

        return results
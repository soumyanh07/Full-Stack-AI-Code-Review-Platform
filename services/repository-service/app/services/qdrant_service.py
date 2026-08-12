from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from app.core.config import settings


class QdrantService:
    """
    Handles vector storage and semantic search using Qdrant.
    """

    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        self.collection = settings.QDRANT_COLLECTION

        self._create_collection()

    def _create_collection(self):
        collections = [
            collection.name
            for collection in self.client.get_collections().collections
        ]

        if self.collection not in collections:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )

    def upsert(
        self,
        points: list[PointStruct],
    ):
        """
        Insert or update vector points.
        """

        if not points:
            return

        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )

    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ):
        """
        Global semantic search.
        """

        result = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
        )

        return result.points

    def search_repository(
        self,
        repository_id: int,
        vector: list[float],
        limit: int = 5,
    ):
        """
        Semantic search restricted to one repository.
        """

        result = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="repository_id",
                        match=MatchValue(
                            value=repository_id,
                        ),
                    ),
                ]
            ),
            with_payload=True,
        )

        return result.points

    def delete_repository(
        self,
        repository_id: int,
    ):
        """
        Delete all vectors belonging to a repository.
        """

        self.client.delete(
            collection_name=self.collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="repository_id",
                        match=MatchValue(
                            value=repository_id,
                        ),
                    ),
                ]
            ),
        )

    def count(self) -> int:
        """
        Return total number of vectors.
        """

        return self.client.count(
            collection_name=self.collection,
        ).count
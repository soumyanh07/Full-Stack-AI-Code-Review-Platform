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
        """
        Create the vector collection if it does not already exist.
        """

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
        Perform semantic vector search across all repositories.
        """

        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
        )

        return response.points

    def search_repository(
        self,
        repository_id: int,
        vector: list[float],
        limit: int = 5,
    ):
        """
        Perform semantic search restricted to one repository.
        """

        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
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
            limit=limit,
        )

        return response.points

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
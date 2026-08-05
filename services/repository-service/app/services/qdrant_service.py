from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)


class QdrantService:
    COLLECTION_NAME = "source_code"

    def __init__(self):
        # Use the Docker Compose service name instead of localhost
        self.client = QdrantClient(
            host="localhost",
            port=6333,
        )

        collections = [
            collection.name
            for collection in self.client.get_collections().collections
        ]

        if self.COLLECTION_NAME not in collections:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    def store_embedding(
        self,
        point_id: int,
        embedding: list,
        payload: dict,
    ):
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload,
                )
            ],
        )

    def search(
        self,
        embedding: list,
        limit: int = 5,
    ):
        return self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=embedding,
            limit=limit,
        ).points

    
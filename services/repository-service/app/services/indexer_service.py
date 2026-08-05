from typing import List, Dict
import uuid

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class IndexerService:
    """
    Handles source code indexing pipeline.

    Flow:
    Source Code
        ↓
    Chunks
        ↓
    Embeddings
        ↓
    Qdrant Vector Database
    """


    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.qdrant_service = QdrantService()



    async def index_files(
        self,
        repository_id: str,
        files: List[Dict]
    ) -> Dict:


        indexed_chunks = 0


        points = []


        for file in files:


            chunks = file.get(
                "chunks",
                []
            )


            for chunk in chunks:


                vector = await self.embedding_service.create_embedding(
                    chunk["content"]
                )


                point = {

                    "id": str(uuid.uuid4()),

                    "vector": vector,

                    "payload": {

                        "repository_id": repository_id,

                        "file_path": file["path"],

                        "language": file.get(
                            "language",
                            "unknown"
                        ),

                        "content": chunk["content"],

                        "chunk_index": chunk.get(
                            "index",
                            0
                        )
                    }
                }


                points.append(point)

                indexed_chunks += 1



        if points:

            await self.qdrant_service.upsert_points(
                points
            )


        return {

            "repository_id": repository_id,

            "indexed_chunks": indexed_chunks,

            "status": "completed"

        }



    async def index_single_file(
        self,
        repository_id: str,
        file_path: str,
        content: str
    ):


        vector = await self.embedding_service.create_embedding(
            content
        )


        point = {

            "id": str(uuid.uuid4()),

            "vector": vector,

            "payload": {

                "repository_id": repository_id,

                "file_path": file_path,

                "content": content

            }
        }


        await self.qdrant_service.upsert_points(
            [point]
        )


        return {

            "file": file_path,

            "status": "indexed"

        }
from __future__ import annotations

import hashlib

from qdrant_client.models import PointStruct

from app.services.github_service import GitHubService
from app.services.file_service import FileService
from app.services.parser_service import ParserService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class IndexerService:
    """
    Coordinates repository indexing.

    Pipeline:

        GitHub repository
            ↓
        Clone repository
            ↓
        Scan source files
            ↓
        Parse files
            ↓
        Chunk source code
            ↓
        Generate embeddings
            ↓
        Store vectors in Qdrant
    """

    def __init__(self):
        self.github = GitHubService()
        self.file_service = FileService()
        self.parser = ParserService()
        self.chunker = ChunkingService()
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()

    def index_repository(
        self,
        repository_id: int,
        repository_url: str,
        owner: str | None = None,
        repository: str | None = None,
    ):
        """
        Clone and index a GitHub repository.

        Args:
            repository_id:
                Database ID of the repository.

            repository_url:
                Git clone URL.

            owner:
                GitHub repository owner.

            repository:
                GitHub repository name.
        """

        # ---------------------------------------------------------
        # Step 1: Determine repository owner/name
        # ---------------------------------------------------------

        if not owner or not repository:
            owner, repository = self._parse_repository_url(
                repository_url
            )

        # ---------------------------------------------------------
        # Step 2: Clone repository
        # ---------------------------------------------------------

        local_path = self.github.clone_repository(
            repository_url,
            owner,
            repository,
        )

        # ---------------------------------------------------------
        # Step 3: Remove previous vectors
        # ---------------------------------------------------------

        self.qdrant.delete_repository(
            repository_id
        )

        # ---------------------------------------------------------
        # Step 4: Scan repository files
        # ---------------------------------------------------------

        files = self.file_service.scan_repository(
            str(local_path)
        )

        total_chunks = 0
        total_vectors = 0

        # ---------------------------------------------------------
        # Step 5: Process every source file
        # ---------------------------------------------------------

        for file_path in files:

            try:
                # ---------------------------------------------
                # Parse file
                # ---------------------------------------------

                parsed = self.parser.parse(
                    file_path
                )

                if not parsed:
                    continue

                content = parsed.get("content", "")

                if not content.strip():
                    continue

                # ---------------------------------------------
                # Chunk document
                # ---------------------------------------------

                chunks = self.chunker.chunk_document(
                    parsed
                )

                if not chunks:
                    continue

                total_chunks += len(chunks)

                # ---------------------------------------------
                # Extract text for embedding
                # ---------------------------------------------

                texts = [
                    chunk["content"]
                    for chunk in chunks
                    if chunk.get("content")
                ]

                if not texts:
                    continue

                # ---------------------------------------------
                # Generate embeddings in batch
                # ---------------------------------------------

                vectors = self.embedding.embed_batch(
                    texts
                )

                # ---------------------------------------------
                # Build Qdrant points
                # ---------------------------------------------

                points = []

                for chunk, vector in zip(
                    chunks,
                    vectors,
                ):

                    point_id = self._generate_point_id(
                        repository_id,
                        chunk,
                    )

                    payload = {
                        "repository_id": repository_id,
                        "filename": chunk["filename"],
                        "path": chunk["path"],
                        "language": chunk["language"],
                        "chunk_id": chunk["chunk_id"],
                        "content": chunk["content"],
                    }

                    points.append(
                        PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload,
                        )
                    )

                # ---------------------------------------------
                # Store vectors in Qdrant
                # ---------------------------------------------

                if points:
                    self.qdrant.upsert(
                        points
                    )

                    total_vectors += len(points)

            except Exception as exc:
                print(
                    f"Failed to index file "
                    f"{file_path}: {exc}"
                )

        # ---------------------------------------------------------
        # Step 6: Return indexing result
        # ---------------------------------------------------------

        return {
            "status": "completed",
            "repository_id": repository_id,
            "repository": f"{owner}/{repository}",
            "files": len(files),
            "chunks": total_chunks,
            "vectors": total_vectors,
        }

    @staticmethod
    def _generate_point_id(
        repository_id: int,
        chunk: dict,
    ) -> str:
        """
        Generate a deterministic Qdrant point ID.

        Using a deterministic ID means re-indexing the same
        repository/chunk does not create duplicate vectors.
        """

        raw_id = (
            f"{repository_id}:"
            f"{chunk['path']}:"
            f"{chunk['chunk_id']}"
        )

        return hashlib.md5(
            raw_id.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _parse_repository_url(
        repository_url: str,
    ) -> tuple[str, str]:
        """
        Extract owner and repository name from a GitHub URL.

        Supported examples:

            https://github.com/user/repository
            https://github.com/user/repository.git
            git@github.com:user/repository.git
        """

        url = repository_url.strip()

        # Remove trailing slash
        url = url.rstrip("/")

        # Handle SSH GitHub URLs
        if url.startswith("git@github.com:"):
            path = url.split(
                "git@github.com:",
                1,
            )[1]

        # Handle HTTPS URLs
        else:
            marker = "github.com/"

            if marker not in url:
                raise ValueError(
                    "Invalid GitHub repository URL: "
                    f"{repository_url}"
                )

            path = url.split(
                marker,
                1,
            )[1]

        parts = [
            part
            for part in path.split("/")
            if part
        ]

        if len(parts) != 2:
            raise ValueError(
                "Could not determine GitHub owner "
                f"and repository from URL: "
                f"{repository_url}"
            )

        owner = parts[0]
        repository = parts[1]

        if repository.endswith(".git"):
            repository = repository[:-4]

        return owner, repository
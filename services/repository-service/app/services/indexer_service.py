from pathlib import Path

from app.services.parser_service import ParserService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class IndexerService:

    EXCLUDED_DIRS = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
        ".idea",
        ".vscode",
    }

    def __init__(self):
        self.parser = ParserService()
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()

    def index_repository(
        self,
        repository_id: int,
        repository_path: str,
    ):
        point_id = repository_id * 1_000_000

        for file in Path(repository_path).rglob("*"):

            if not file.is_file():
                continue

            if any(
                part in self.EXCLUDED_DIRS
                for part in file.parts
            ):
                continue

            text = self.parser.read_file(str(file))

            if not text:
                continue

            chunks = self.chunk_text(text)

            for chunk_no, chunk in enumerate(chunks):

                embedding = self.embedding.generate_embedding(chunk)

                self.qdrant.store_embedding(
                    point_id=point_id,
                    embedding=embedding,
                    payload={
                        "repository_id": repository_id,
                        "path": str(file),
                        "chunk": chunk_no,
                        "text": chunk,
                    },
                )

                point_id += 1

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        chunks = []

        start = 0

        while start < len(text):

            end = min(start + chunk_size, len(text))

            chunks.append(text[start:end])

            start += chunk_size - overlap

        return chunks
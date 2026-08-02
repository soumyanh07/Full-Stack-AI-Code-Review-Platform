from app.repositories.source_file_repository import SourceFileRepository
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.parser_service import ParserService
from app.services.qdrant_service import QdrantService


class IndexingService:
    def __init__(self, db):
        self.repository = SourceFileRepository(db)
        self.parser = ParserService()
        self.chunker = ChunkingService()
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()

    def index_repository(self, repository_id, files):
        indexed = 0

        for file_path in files:

            content = self.parser.read_file(file_path)

            if content is None:
                continue

            parsed = None

            if file_path.endswith(".py"):
                parsed = self.parser.parse_python_file(file_path)

            source_file = self.repository.create_source_file(
                repository_id=repository_id,
                file_path=file_path,
                language=file_path.split(".")[-1],
                content=content,
                metadata=parsed,
            )

            chunks = self.chunker.chunk_text(content)

            for index, chunk in enumerate(chunks):

                embedding = self.embedding.generate_embedding(chunk)

                self.qdrant.store_embedding(
                    point_id=(source_file.id * 10000) + index,
                    embedding=embedding,
                    payload={
                        "repository_id": repository_id,
                        "source_file_id": source_file.id,
                        "path": file_path,
                        "chunk": index,
                        "text": chunk,
                    },
                )

            indexed += 1

        return indexed
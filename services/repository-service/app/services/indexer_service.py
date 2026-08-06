from app.services.github_service import GitHubService
from app.services.file_service import FileService
from app.services.parser_service import ParserService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class IndexerService:

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
    ):

        # Step 1
        local_path = self.github.clone_repository(
            repository_url
        )

        # Step 2
        files = self.file_service.scan_repository(
            local_path
        )

        for file in files:

            # Step 3
            parsed = self.parser.parse_file(file)

            if not parsed:
                continue

            # Step 4
            chunks = self.chunker.chunk(
                parsed
            )

            # Step 5
            vectors = self.embedding.embed(
                repository_id,
                file,
                chunks,
            )

            # Step 6
            self.qdrant.upsert(vectors)

        return {
            "status": "completed",
            "files": len(files),
        }
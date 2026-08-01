from app.repositories.source_file_repository import SourceFileRepository
from app.services.parser_service import ParserService


class IndexingService:
    def __init__(self, db):
        self.repository = SourceFileRepository(db)
        self.parser = ParserService()

    def index_repository(self, repository_id: int, files: list[str]) -> int:
        indexed = 0

        for file_path in files:
            # Read file content
            content = self.parser.read_file(file_path)

            if content is None:
                continue

            # Parse only Python files
            metadata = None
            if file_path.endswith(".py"):
                metadata = self.parser.parse_python_file(file_path)

            # Save file in PostgreSQL
            self.repository.create_source_file(
                repository_id=repository_id,
                file_path=file_path,
                language=file_path.split(".")[-1].lower(),
                content=content,
                metadata=metadata,
            )

            indexed += 1

        return indexed
from app.services.parser_service import ParserService
from app.services.file_service import FileService
from app.repositories.source_file_repository import SourceFileRepository


class IndexingService:

    def __init__(self, db):
        self.files = FileService()
        self.parser = ParserService()
        self.source_repository = SourceFileRepository(db)

    def index_repository(
        self,
        repository_id: int,
        local_path: str,
    ):
        scanned_files = self.files.scan_repository(local_path)

        indexed = 0

        for file in scanned_files:

            parsed = self.parser.parse_file(file)

            self.source_repository.create_file(
                repository_id=repository_id,
                path=parsed["path"],
                language=parsed["language"],
                content=parsed["content"],
            )

            indexed += 1

        return indexed
from sqlalchemy.orm import Session

from app.models.source_file import SourceFile


class SourceFileRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_source_file(
        self,
        repository_id: int,
        file_path: str,
        language: str,
        content: str,
        metadata=None,
    ):
        source_file = SourceFile(
            repository_id=repository_id,
            path=file_path,
            language=language,
            content=content,
            source_metadata=metadata,
        )

        self.db.add(source_file)
        self.db.commit()
        self.db.refresh(source_file)

        return source_file

    def create_file(
        self,
        repository_id: int,
        file_path: str,
        language: str,
        content: str,
        metadata=None,
    ):
        return self.create_source_file(
            repository_id=repository_id,
            file_path=file_path,
            language=language,
            content=content,
            metadata=metadata,
        )

    def get_repository_files(
        self,
        repository_id: int,
    ):
        return (
            self.db.query(SourceFile)
            .filter(
                SourceFile.repository_id == repository_id
            )
            .all()
        )
from sqlalchemy.orm import Session

from app.models.source_file import SourceFile


class SourceFileRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_file(
        self,
        repository_id: int,
        path: str,
        language: str,
        content: str,
    ):
        file = SourceFile(
            repository_id=repository_id,
            path=path,
            language=language,
            content=content,
        )

        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)

        return file

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
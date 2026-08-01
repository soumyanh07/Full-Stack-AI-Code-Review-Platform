from pathlib import Path

from app.utils.file_utils import (
    is_supported_file,
    should_ignore,
)


class FileService:

    def scan_repository(self, repository_path: str):
        repository = Path(repository_path)

        files = []

        for file in repository.rglob("*"):

            if file.is_dir():
                continue

            if should_ignore(file):
                continue

            if not is_supported_file(file):
                continue

            files.append(str(file))

        return files
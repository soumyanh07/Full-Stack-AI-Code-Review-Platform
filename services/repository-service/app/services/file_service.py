from __future__ import annotations

from pathlib import Path


class FileService:
    """
    Scans repositories and returns source code files.
    """

    IGNORE_DIRS = {
        ".git",
        ".github",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".idea",
        ".vscode",
        ".next",
        ".pytest_cache",
    }

    IGNORE_SUFFIXES = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".exe",
        ".dll",
        ".so",
        ".class",
        ".jar",
        ".pyc",
    }

    def scan_repository(
        self,
        repository_path: str,
    ) -> list[Path]:

        root = Path(repository_path)

        files = []

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            if any(part in self.IGNORE_DIRS for part in file.parts):
                continue

            if file.suffix.lower() in self.IGNORE_SUFFIXES:
                continue

            files.append(file)

        return sorted(files)

    def read_file(
        self,
        path: Path,
    ) -> str:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def file_extension(
        self,
        path: Path,
    ) -> str:

        return path.suffix.lower()
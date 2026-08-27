from __future__ import annotations

from pathlib import Path


class ParserService:
    """
    Detects programming languages and extracts file metadata.
    """

    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".java": "java",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".c": "c",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".rb": "ruby",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
        ".sql": "sql",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".md": "markdown",
        ".dockerfile": "docker",
    }

    def language(self, path: Path) -> str:
        suffix = path.suffix.lower()

        if path.name.lower() == "dockerfile":
            return "docker"

        return self.LANGUAGE_MAP.get(
            suffix,
            "text",
        )

    def metadata(self, path: Path) -> dict:

        return {
            "filename": path.name,
            "extension": path.suffix.lower(),
            "language": self.language(path),
            "path": str(path),
        }

    def parse(
        self,
        path: Path,
    ) -> dict:

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return {
            **self.metadata(path),
            "content": content,
        }
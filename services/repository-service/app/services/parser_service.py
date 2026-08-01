from pathlib import Path


class ParserService:

    EXTENSIONS = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "React",
        ".jsx": "React",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".xml": "XML",
        ".md": "Markdown",
        ".sql": "SQL",
    }

    def parse_file(self, file_path: str):
        path = Path(file_path)

        language = self.EXTENSIONS.get(
            path.suffix.lower(),
            "Unknown",
        )

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                content = file.read()
        except Exception:
            content = ""

        return {
            "path": str(path),
            "language": language,
            "content": content,
        }
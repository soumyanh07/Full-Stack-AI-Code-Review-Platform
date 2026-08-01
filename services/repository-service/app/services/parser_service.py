from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_python


class ParserService:
    SUPPORTED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".html",
        ".css",
        ".json",
        ".yaml",
        ".yml",
        ".md",
        ".sql",
        ".xml",
        ".sh",
    }

    def __init__(self):
        self.parser = Parser()
        self.parser.language = Language(tree_sitter_python.language())

    def read_file(self, file_path: str):
        path = Path(file_path)

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return None

        try:
            return path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            return None

    def parse_python_file(self, file_path: str):
        code = self.read_file(file_path)

        if code is None:
            return None

        tree = self.parser.parse(code.encode("utf-8"))
        root = tree.root_node

        functions = []
        classes = []
        imports = []

        self._walk(
            root,
            code,
            functions,
            classes,
            imports,
        )

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
        }

    def _walk(
        self,
        node,
        code,
        functions,
        classes,
        imports,
    ):
        if node.type == "function_definition":
            functions.append({
                "text": code[node.start_byte:node.end_byte],
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
            })

        elif node.type == "class_definition":
            classes.append({
                "text": code[node.start_byte:node.end_byte],
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
            })

        elif node.type in (
            "import_statement",
            "import_from_statement",
        ):
            imports.append(
                code[node.start_byte:node.end_byte]
            )

        for child in node.children:
            self._walk(
                child,
                code,
                functions,
                classes,
                imports,
            )
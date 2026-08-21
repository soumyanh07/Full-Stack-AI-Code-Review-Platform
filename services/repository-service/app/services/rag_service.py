from __future__ import annotations

from app.services.search_service import SearchService


class RAGService:
    """
    Retrieves relevant repository context for LLM prompts.
    """

    def __init__(self):
        self.search = SearchService()

    def retrieve(
        self,
        repository_id: int,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        return self.search.search(
            repository_id=repository_id,
            query=query,
            limit=limit,
        )

    def build_context(
        self,
        repository_id: int,
        query: str,
        limit: int = 5,
    ) -> str:

        results = self.retrieve(
            repository_id=repository_id,
            query=query,
            limit=limit,
        )

        if not results:
            return (
                "NO_RELEVANT_CONTEXT_FOUND"
            )

        sections = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            sections.append(
                f"""
--- Context {index} ---

File:
{result.get("path", "unknown")}

Language:
{result.get("language", "unknown")}

Similarity:
{result.get("score", 0.0):.4f}

Code:
{result.get("content", "")}
""".strip()
            )

        return "\n\n".join(sections)
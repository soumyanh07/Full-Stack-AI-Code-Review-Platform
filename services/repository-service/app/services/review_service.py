from app.services.llm_service import LLMService
from app.services.search_service import SearchService


class ReviewService:

    def __init__(self):
        self.search = SearchService()
        self.llm = LLMService()

    def review(self, query: str, limit: int = 5):
        # First try to retrieve repository context.
        results = self.search.search(
            query=query,
            limit=limit,
        )

        context = "\n\n".join(
            point.payload["text"]
            for point in results
            if point.payload.get("text")
        )

        # For PR reviews, the GitHub patch itself is the
        # authoritative source. If semantic search finds
        # nothing, review the supplied patch directly.
        if not context.strip():
            context = query

        prompt = f"""
You are a senior software engineer performing a GitHub pull-request review.

Review the following Git diff / source code carefully.

Focus on:
- Bugs and logic errors
- Security vulnerabilities
- Performance problems
- Error handling
- Clean code
- Maintainability
- Best practices

Important:
- Analyze the actual code provided below.
- Do not say that source code was not provided.
- If the code is correct, explicitly say so.
- Distinguish real problems from optional improvements.

Provide:

1. Summary
2. Bugs
3. Security Issues
4. Performance Improvements
5. Code Quality Suggestions

GitHub Diff / Source Code:

{context}
"""

        review = self.llm.review(prompt)

        return {
            "review": review,
            "chunks": len(results),
        }
from app.services.llm_service import LLMService
from app.services.search_service import SearchService


class ReviewService:

    def __init__(self):
        self.search = SearchService()
        self.llm = LLMService()

    def review(self, query: str, limit: int = 5):

        # Retrieve relevant code chunks
        results = self.search.search(
            query=query,
            limit=limit,
        )

        # Build context from retrieved chunks
        context = "\n\n".join(
            point.payload["text"]
            for point in results
        )

        prompt = f"""
You are a senior software engineer.

Review the following source code.

Focus on:

- Bugs
- Security
- Performance
- Clean Code
- Best Practices

Provide:
1. Summary
2. Bugs
3. Security Issues
4. Performance Improvements
5. Code Quality Suggestions

Source Code:

{context}
"""

        review = self.llm.review(prompt)

        return {
            "review": review,
            "chunks": len(results),
        }
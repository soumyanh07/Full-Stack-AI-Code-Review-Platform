from __future__ import annotations

from app.clients.ollama_client import OllamaClient


class ReviewService:
    """
    AI-powered code review service.
    """

    def __init__(self):
        self.ollama = OllamaClient()

    def review_code(
        self,
        code: str,
        language: str = "python",
    ) -> dict:
        """
        Review a code snippet using Ollama.
        """
        prompt = f"""You are a Senior Software Engineer.

Review the following {language} code.

Focus on:
1. Bugs
2. Security Issues
3. Performance
4. Readability
5. Maintainability
6. Best Practices
7. Code Smells
8. Possible Improvements

Return the response in Markdown.

Code:

```{language}
{code}
```"""

        try:
            review = self.ollama.generate(prompt).strip()

            return {
                "success": True,
                "review": review,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
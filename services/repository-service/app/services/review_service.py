from __future__ import annotations

from app.services.llm_service import LLMService


class ReviewService:
    """
    AI-powered code review service.

    Sends source code to the configured LLM and returns
    actionable software-engineering feedback.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def review(
        self,
        code: str,
        language: str = "text",
    ) -> dict:
        """
        Review a piece of source code.
        """

        if not code or not code.strip():
            return {
                "language": language,
                "review": "No code was provided for review.",
            }

        review = self.llm_service.review_code(
            code=code,
            language=language,
        )

        return {
            "language": language,
            "review": review,
        }
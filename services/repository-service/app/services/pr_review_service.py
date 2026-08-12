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
        filename: str | None = None,
    ) -> dict:
        """
        Review a piece of source code.

        Args:
            code: Source code to review.
            language: Programming language of the source code.
            filename: Optional source filename.

        Returns:
            Dictionary containing language, filename, and review.
        """

        if not code or not code.strip():
            return {
                "language": language,
                "filename": filename,
                "review": "No code was provided for review.",
            }

        review = self.llm_service.review_code(
            code=code,
            language=language,
            filename=filename,
        )

        return {
            "language": language,
            "filename": filename,
            "review": review,
        }
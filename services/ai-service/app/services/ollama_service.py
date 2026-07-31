import httpx

from app.core.config import settings
from app.schemas.ai import AnalyzeRequest, AnalyzeResponse


class OllamaService:

    def analyze(
        self,
        request: AnalyzeRequest,
    ) -> AnalyzeResponse:

        prompt = f"""
You are an expert software engineer.

Review the following Python code.

Code:

{request.code}

Provide:

1. Summary
2. Bugs
3. Improvements
4. Best Practices
5. Corrected Code
"""

        response = httpx.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": settings.MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return AnalyzeResponse(
            review=data["response"]
        )
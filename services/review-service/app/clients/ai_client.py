import httpx

from app.core.config import settings


class AIClient:

    def analyze(self, code: str) -> str:
        response = httpx.post(
            f"{settings.AI_SERVICE}/api/v1/analyze",
            json={
                "code": code,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data["review"]
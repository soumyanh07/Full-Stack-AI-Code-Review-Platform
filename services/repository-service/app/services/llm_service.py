from __future__ import annotations

import requests

from app.core.config import settings


class LLMService:
    """
    Ollama-based local LLM service.

    Handles:
    - General text generation
    - Conversational chat
    - AI-powered code reviews
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL

    def generate(
        self,
        prompt: str,
        timeout: int = 300,
    ) -> str:
        """
        Generate text using Ollama's /api/generate endpoint.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=timeout,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    def chat(
        self,
        messages: list[dict],
        timeout: int = 300,
    ) -> str:
        """
        Send a conversation to Ollama's /api/chat endpoint.
        """

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
            },
            timeout=timeout,
        )

        response.raise_for_status()

        data = response.json()

        return (
            data.get("message", {})
            .get("content", "")
            .strip()
        )

    def review_code(
        self,
        code: str,
        language: str = "text",
        filename: str | None = None,
        timeout: int = 600,
    ) -> str:
        """
        Perform an AI-powered code review.
        """

        filename_context = (
            f"Filename: {filename}"
            if filename
            else "Filename: not provided"
        )

        prompt = f"""You are a senior software engineer performing a precise code review.

Review ONLY the code provided below.

{filename_context}

Language: {language}

CODE:
```{language}
{code}
```

Provide constructive feedback on:
- Code quality and style
- Potential bugs or issues
- Performance considerations
- Best practices
"""

        return self.generate(
            prompt,
            timeout=timeout,
        )
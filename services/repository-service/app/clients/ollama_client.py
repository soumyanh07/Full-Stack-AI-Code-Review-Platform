from __future__ import annotations

import ollama

from app.core.config import settings


class OllamaClient:
    """
    Client for communicating with the Ollama API.
    """

    def __init__(self):
        self.client = ollama.Client(
            host=settings.OLLAMA_URL
        )

        self.model = settings.OLLAMA_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an LLM response.
        """

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
        )

        return response["response"]
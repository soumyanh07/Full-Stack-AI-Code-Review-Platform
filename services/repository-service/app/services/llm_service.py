from __future__ import annotations

import json
import requests

from app.core.config import settings


class LLMService:
    """
    Ollama-based local LLM service.

    Handles:
    - General text generation
    - Conversational chat
    - Structured AI code reviews
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

    def generate_json(
        self,
        prompt: str,
        timeout: int = 600,
    ) -> dict:
        """
        Generate structured JSON using Ollama.
        """
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=timeout,
        )

        response.raise_for_status()
        data = response.json()
        content = data.get("response", "").strip()

        if not content:
            raise ValueError("Ollama returned an empty response.")

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Ollama returned invalid JSON: {content}"
            ) from exc

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
    ) -> dict:
        """
        Perform a structured AI-powered code review.
        """
        filename_context = (
            f"Filename: {filename}"
            if filename
            else "Filename: not provided"
        )

        prompt = f"""You are a senior software engineer performing a precise code review.

Review ONLY the source code provided below.

{filename_context}

Language: {language}

CODE:
```{language}
{code}
```

Analyze the code for:

1. Bugs and correctness issues
2. Security vulnerabilities
3. Performance problems
4. Code quality and style
5. Maintainability
6. Best practices

Return ONLY valid JSON.
Use exactly this structure:
{{
  "summary": "Short overall assessment of the code.",
  "score": 0,
  "issues": [
    {{
      "severity": "critical",
      "category": "security",
      "line": 1,
      "message": "Clear explanation of the issue.",
      "suggestion": "Specific recommendation to fix it."
    }}
  ]
}}

Rules:

* score must be an integer from 0 to 10.
* severity must be one of: critical, high, medium, low, info.
* category must be one of: bug, security, performance, style, maintainability, best_practice.
* line must be the relevant source-code line number when possible.
* Use null for line when a specific line cannot be identified.
* Do not invent issues.
* Keep issues concise and actionable.
* Return ONLY JSON."""

        return self.generate_json(
            prompt,
            timeout=timeout,
        )
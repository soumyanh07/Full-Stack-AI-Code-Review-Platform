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
    ) -> str:
        """
        Generate a response using Ollama's /api/generate endpoint.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "",
        ).strip()

    def chat(
        self,
        messages: list[dict],
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
            timeout=300,
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
    ) -> str:
        """
        Perform an AI-powered code review.
        """

        prompt = f"""
You are a senior software engineer performing a professional
code review.

Review ONLY the code provided below.

Analyze the code for:

1. Bugs
2. Security vulnerabilities
3. Performance issues
4. Maintainability
5. Code quality
6. Error handling
7. Best practices

Important rules:

- Do not invent bugs that are not supported by the provided code.
- Do not assume a function must be called just because it is defined.
- Do not recommend unnecessary validation.
- Do not recommend unnecessary error handling.
- Do not recommend changes merely for the sake of changing the code.
- Distinguish actual problems from optional improvements.
- If a category has no issue, explicitly say:
  "No significant issue found."
- Give specific and actionable feedback.
- Reference the relevant code when possible.
- Keep the review concise and technically accurate.
- Prioritize real problems over stylistic preferences.

Return the review using exactly this structure:

## Summary

Brief overall assessment of the code.

## Bugs

List only actual bugs.

If none:
No significant issue found.

## Security

List only actual security vulnerabilities.

If none:
No significant issue found.

## Performance

List meaningful performance concerns.

If none:
No significant issue found.

## Maintainability

List maintainability concerns and useful improvements.

## Code Quality

Discuss readability, structure, style, and correctness.

## Error Handling

Discuss missing or inappropriate error handling
only when relevant.

## Best Practices

Give relevant best-practice recommendations.

## Suggested Improvement

Provide an improved version of the code only when
there is a meaningful improvement.

Language: {language}

Code:

```{language}
{code}
```
"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=600,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "",
        ).strip()
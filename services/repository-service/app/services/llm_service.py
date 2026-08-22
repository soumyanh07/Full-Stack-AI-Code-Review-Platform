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
            raise ValueError(
                "Ollama returned an empty response."
            )

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

        The LLM is instructed to return JSON matching
        the application's review schema.
        """

        if not code or not code.strip():
            return {
                "summary": "No code was provided for review.",
                "score": 10,
                "issues": [],
            }

        filename_context = (
            f"Filename: {filename}"
            if filename
            else "Filename: not provided"
        )

        prompt = f"""
You are a senior software engineer performing a precise code review.

Review ONLY the source code provided below.

{filename_context}

Language: {language}

SOURCE CODE:
```{language}
{code}
```

Analyze ONLY the provided source code for:

Bugs and correctness issues
Security vulnerabilities
Performance problems
Code quality and style
Maintainability
Best practices

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

score must be an integer from 0 to 10.
severity must be one of:
critical, high, medium, low, info
category must be one of:
bug, security, performance, style, maintainability, best_practice
line must be the relevant source-code line number when possible.
Use null when a specific line cannot be identified.
Do not invent issues.
Do not review code that is not present.
Keep issues concise and actionable.
issues must always be an array.

Return ONLY JSON.
""".strip()

        result = self.generate_json(
            prompt=prompt,
            timeout=timeout,
        )

        summary = result.get(
            "summary",
            "No summary was generated.",
        )

        score = result.get("score", 0)

        issues = result.get("issues", [])

        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

        score = max(0, min(10, score))

        if not isinstance(issues, list):
            issues = []

        valid_severities = {
            "critical",
            "high",
            "medium",
            "low",
            "info",
        }

        valid_categories = {
            "bug",
            "security",
            "performance",
            "style",
            "maintainability",
            "best_practice",
        }

        normalized_issues = []

        for issue in issues:
            if not isinstance(issue, dict):
                continue

            severity = issue.get(
                "severity",
                "info",
            )

            category = issue.get(
                "category",
                "best_practice",
            )

            if severity not in valid_severities:
                severity = "info"

            if category not in valid_categories:
                category = "best_practice"

            line = issue.get("line")

            if line is not None:
                try:
                    line = int(line)

                    if line < 1:
                        line = None

                except (TypeError, ValueError):
                    line = None

            message = str(
                issue.get(
                    "message",
                    "No issue description provided.",
                )
            ).strip()

            suggestion = str(
                issue.get(
                    "suggestion",
                    "No suggestion provided.",
                )
            ).strip()

            if not message:
                continue

            if not suggestion:
                suggestion = "Review and improve this code."

            normalized_issues.append(
                {
                    "severity": severity,
                    "category": category,
                    "line": line,
                    "message": message,
                    "suggestion": suggestion,
                }
            )

        return {
            "summary": str(summary).strip(),
            "score": score,
            "issues": normalized_issues,
        }
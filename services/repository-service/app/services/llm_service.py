from __future__ import annotations

import json

import requests

from app.core.config import settings


class LLMService:
    """
    Ollama-based local LLM service.

    Handles:
    - General text generation
    - Structured JSON generation
    - Conversational chat
    - Structured AI code reviews
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL

    # =========================================================
    # GENERAL GENERATION
    # =========================================================

    def generate(
        self,
        prompt: str,
        timeout: int = 180,
    ) -> str:
        """
        Generate text using Ollama's /api/generate endpoint.

        Generation is intentionally bounded so the local LLM
        does not spend several minutes producing unnecessarily
        long responses.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.1,
                },
            },
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    # =========================================================
    # JSON GENERATION
    # =========================================================

    def generate_json(
        self,
        prompt: str,
        timeout: int = 180,
    ) -> dict:
        """
        Generate structured JSON using Ollama.

        Used primarily for AI code reviews.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "num_predict": 350,
                    "temperature": 0.2,
                },
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
            result = json.loads(content)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Ollama returned invalid JSON: {content}"
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "Ollama JSON response must be an object."
            )

        return result

    # =========================================================
    # CHAT
    # =========================================================

    def chat(
        self,
        messages: list[dict],
        timeout: int = 180,
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
                "options": {
                    "num_predict": 200,
                    "temperature": 0.2,
                },
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

    # =========================================================
    # CODE REVIEW
    # =========================================================

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
You are a senior software engineer performing a code review.

Review ONLY the code provided below.

Do not assume that code exists outside the provided input.
Do not invent bugs, security issues, configuration problems,
dependencies, or behavior.

{filename_context}
Language: {language}

CODE:
```{language}
{code}
```

Check only for:

- correctness bugs
- real security vulnerabilities
- performance problems
- style problems that materially affect readability
- maintainability problems
- important best-practice violations

IMPORTANT RULES:

- Report an issue only when it is clearly supported by the
  provided code.
- Do not report hypothetical problems.
- Do not report SSL/TLS issues for localhost HTTP endpoints.
- Do not claim a parameter is unused unless the provided code
  proves that it is unused.
- Use the actual line number when possible.
- Return at most 5 issues.
- If there are no meaningful issues, return an empty issues array.
- Score the code from 0 to 10.
- The score should reflect the quality of the provided code.

Return ONLY valid JSON using exactly this structure:

{{
  "summary": "Short overall assessment.",
  "score": 0,
  "issues": [
    {{
      "severity": "critical|high|medium|low|info",
      "category": "bug|security|performance|style|maintainability|best_practice",
      "line": 1,
      "message": "Specific issue supported by the code.",
      "suggestion": "Specific fix."
    }}
  ]
}}
""".strip()

        try:
            result = self.generate_json(
                prompt=prompt,
                timeout=timeout,
            )
        except ValueError:
            retry_prompt = f"""
Return ONLY one valid JSON object.

No markdown.
No explanation.
No text before or after the JSON.
Do not repeat any JSON key.

Required structure:

{{
  "summary": "Short overall assessment.",
  "score": 0,
  "issues": []
}}

Rules:
- score must be an integer from 0 to 10
- issues must be an array
- maximum 5 issues
- each issue must contain:
  severity, category, line, message, suggestion
- only report issues directly supported by the supplied code

Filename: {filename or "not provided"}
Language: {language}

CODE:
```{language}
{code}
```

""".strip()

            result = self.generate_json(
                prompt=retry_prompt,
                timeout=timeout,
            )

        # -----------------------------------------------------
        # Normalize summary
        # -----------------------------------------------------

        summary = result.get(
            "summary",
            "No summary was generated.",
        )

        summary = str(summary).strip()

        if not summary:
            summary = "No summary was generated."

        # -----------------------------------------------------
        # Normalize score
        # -----------------------------------------------------

        score = result.get("score", 0)

        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

        score = max(0, min(10, score))

        # -----------------------------------------------------
        # Normalize issues
        # -----------------------------------------------------

        issues = result.get("issues", [])

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

            # -------------------------------------------------
            # Validate severity
            # -------------------------------------------------

            if severity not in valid_severities:
                severity = "info"

            # -------------------------------------------------
            # Validate category
            # -------------------------------------------------

            if category not in valid_categories:
                category = "best_practice"

            # -------------------------------------------------
            # Validate line number
            # -------------------------------------------------

            line = issue.get("line")

            if line is not None:

                try:
                    line = int(line)

                    if line < 1:
                        line = None

                except (TypeError, ValueError):
                    line = None

            # -------------------------------------------------
            # Normalize message
            # -------------------------------------------------

            message = str(
                issue.get(
                    "message",
                    "No issue description provided.",
                )
            ).strip()

            if not message:
                continue

            # -------------------------------------------------
            # Normalize suggestion
            # -------------------------------------------------

            suggestion = str(
                issue.get(
                    "suggestion",
                    "No suggestion provided.",
                )
            ).strip()

            if not suggestion:
                suggestion = (
                    "Review and improve this code."
                )

            normalized_issues.append(
                {
                    "severity": severity,
                    "category": category,
                    "line": line,
                    "message": message,
                    "suggestion": suggestion,
                }
            )

            # -------------------------------------------------
            # Hard limit
            # -------------------------------------------------

            if len(normalized_issues) >= 5:
                break

        # -----------------------------------------------------
        # Final normalized result
        # -----------------------------------------------------

        return {
            "summary": summary,
            "score": score,
            "issues": normalized_issues,
        }
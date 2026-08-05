from typing import List, Dict
import json

from app.services.llm_service import LLMService


class AIReviewService:
    """
    Handles AI-powered code review generation.
    """

    def __init__(self):
        self.llm = LLMService()

    async def review_code(
        self,
        file_path: str,
        code: str,
        language: str = "python"
    ) -> Dict:

        prompt = f"""
You are an expert senior software engineer.

Review the following {language} code.

File:
{file_path}

Code:
{code}

Provide:
1. Bugs
2. Security issues
3. Performance problems
4. Code quality improvements
5. Best practices

Return JSON format:

{{
    "issues": [
        {{
            "type": "bug/security/performance/style",
            "line": number,
            "severity": "low/medium/high",
            "message": "",
            "suggestion": ""
        }}
    ],
    "summary": ""
}}
"""

        response = await self.llm.generate(prompt)

        try:
            return json.loads(response)

        except Exception:
            return {
                "issues": [],
                "summary": response
            }


    async def review_repository(
        self,
        files: List[Dict]
    ) -> Dict:

        reviews = []

        for file in files:
            result = await self.review_code(
                file_path=file["path"],
                code=file["content"],
                language=file.get("language", "python")
            )

            reviews.append(
                {
                    "file": file["path"],
                    "review": result
                }
            )

        return {
            "files_reviewed": len(files),
            "reviews": reviews
        }
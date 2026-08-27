from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=100000,
    )

    language: str = Field(
        default="text",
        min_length=1,
        max_length=50,
    )

    filename: str | None = None


class ReviewIssue(BaseModel):
    severity: Literal["critical", "high", "medium", "low", "info"]
    category: Literal[
        "bug",
        "security",
        "performance",
        "style",
        "maintainability",
        "best_practice",
    ]
    line: int | None = None
    message: str = Field(min_length=1)
    suggestion: str = Field(min_length=1)


class ReviewResponse(BaseModel):
    language: str
    filename: str | None = None
    summary: str
    score: int = Field(ge=0, le=10)
    issues: list[ReviewIssue] = Field(default_factory=list)
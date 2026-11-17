from __future__ import annotations

import hashlib
import hmac
import json

from fastapi import APIRouter, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.outbox_event import OutboxEvent
from app.services.repository_service import RepositoryService

from app.core.config import settings
from app.tasks.review_pull_request import review_pull_request


router = APIRouter(
    prefix="/webhooks",
    tags=["GitHub Webhooks"],
)


def _verify_signature(
    body: bytes,
    signature: str | None,
) -> bool:
    """
    Verify GitHub webhook HMAC SHA-256 signature.
    """

    webhook_secret = settings.GITHUB_WEBHOOK_SECRET.strip()
    environment = settings.ENVIRONMENT.strip().lower()

    # During local development, allow webhooks when
    # no secret has been configured yet.
    if not webhook_secret:
        return environment == "development"

    if not signature:
        return False

    expected_signature = (
        "sha256="
        + hmac.new(
            webhook_secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()
    )

    return hmac.compare_digest(
        expected_signature,
        signature,
    )


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(
        default="",
    ),
    x_hub_signature_256: str | None = Header(
        default=None,
    ),
):
    """
    Handle GitHub webhook events.

    Supported events:

    - push
    - pull_request
    """

    body = await request.body()

    # ------------------------------------------------------------
    # Verify GitHub signature
    # ------------------------------------------------------------

    if not _verify_signature(
        body,
        x_hub_signature_256,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid GitHub webhook signature",
        )

    # ------------------------------------------------------------
    # Parse payload
    # ------------------------------------------------------------

    try:
        payload = json.loads(
            body.decode("utf-8")
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload",
        )

    # ------------------------------------------------------------
    # Ignore unsupported events
    # ------------------------------------------------------------

    if x_github_event not in {
        "push",
        "pull_request",
    }:
        return {
            "status": "ignored",
            "event": x_github_event,
        }

    repository = payload.get("repository")

    if not isinstance(repository, dict):
        raise HTTPException(status_code=400, detail="Repository missing")

    owner_data = repository.get("owner") or {}
    github_owner = owner_data.get("login")
    github_name = repository.get("name")

    if not github_owner or not github_name:
        raise HTTPException(status_code=400, detail="Repository identity missing")

    db = SessionLocal()
    try:
        registered_repositories = (
            RepositoryService(db).get_registered_github_repositories(
                github_owner,
                github_name,
            )
        )
        registered_targets = [
            (repository.id, repository.url)
            for repository in registered_repositories
        ]

        if x_github_event == "push":
            db.add_all([
                OutboxEvent(
                    repository_id=repository.id,
                    event_type="repository.index",
                )
                for repository in registered_repositories
            ])
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    if not registered_targets:
        return {
            "status": "ignored",
            "reason": "Repository is not registered on this platform",
        }

    # ============================================================
    # PULL REQUEST EVENT
    # ============================================================

    if x_github_event == "pull_request":
        action = payload.get(
            "action",
            "",
        )

        # Only review PRs when they are opened,
        # reopened, or updated with new commits.
        if action not in {
            "opened",
            "reopened",
            "synchronize",
        }:
            return {
                "status": "ignored",
                "event": x_github_event,
                "action": action,
            }

        owner = github_owner
        repository_name = github_name

        pull_request = payload.get(
            "pull_request",
            {},
        )

        pull_number = pull_request.get(
            "number"
        )

        if not owner:
            raise HTTPException(
                status_code=400,
                detail="Repository owner missing",
            )

        if not repository_name:
            raise HTTPException(
                status_code=400,
                detail="Repository name missing",
            )

        if not pull_number:
            raise HTTPException(
                status_code=400,
                detail="Pull Request number missing",
            )

        task = review_pull_request.delay(
            owner,
            repository_name,
            pull_number,
        )

        return {
            "status": "queued",
            "event": x_github_event,
            "action": action,
            "owner": owner,
            "repository": repository_name,
            "pr_number": pull_number,
            "task_id": task.id,
        }

    # ============================================================
    # PUSH EVENT
    # ============================================================

    return {
        "status": "accepted",
        "event": x_github_event,
        "registered_copies": len(registered_targets),
        "dispatch": "outbox",
    }

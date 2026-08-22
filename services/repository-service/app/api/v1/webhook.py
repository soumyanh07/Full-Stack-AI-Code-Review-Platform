from __future__ import annotations

import hashlib
import hmac
import json

from fastapi import APIRouter, Header, HTTPException, Request

from app.core.config import settings
from app.tasks.index_repository import index_repository
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

    webhook_secret = getattr(
        settings,
        "GITHUB_WEBHOOK_SECRET",
        "",
    )

    # During local development, allow webhooks when
    # no secret has been configured yet.
    if not webhook_secret:
        return True

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

    repository = payload.get(
        "repository"
    )

    if repository is None:
        raise HTTPException(
            status_code=400,
            detail="Repository missing",
        )

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

        owner_data = repository.get(
            "owner",
            {},
        )

        owner = owner_data.get(
            "login"
        )

        repository_name = repository.get(
            "name"
        )

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

    repository_id = repository.get(
        "id"
    )

    clone_url = repository.get(
        "clone_url"
    )

    if repository_id is None:
        raise HTTPException(
            status_code=400,
            detail="Repository ID missing",
        )

    if not clone_url:
        raise HTTPException(
            status_code=400,
            detail="Clone URL missing",
        )

    task = index_repository.delay(
        repository_id,
        clone_url,
    )

    return {
        "status": "queued",
        "event": x_github_event,
        "task_id": task.id,
    }
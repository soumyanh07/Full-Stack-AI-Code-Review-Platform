from fastapi import APIRouter, Header, HTTPException

from app.tasks.index_repository import (
    index_repository,
)


router = APIRouter(
    prefix="/webhooks",
    tags=["GitHub Webhooks"],
)


@router.post("/github")
async def github_webhook(
    payload: dict,
    x_github_event: str = Header(
        default=""
    ),
):

    if x_github_event not in {
        "push",
        "pull_request",
    }:
        return {
            "status": "ignored"
        }

    repository = payload.get(
        "repository"
    )

    if repository is None:
        raise HTTPException(
            status_code=400,
            detail="Repository missing",
        )

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
        "task_id": task.id,
        "event": x_github_event,
    }
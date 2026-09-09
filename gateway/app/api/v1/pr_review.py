import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.proxy import ProxyClient

logger = logging.getLogger("gateway.pr_review")

router = APIRouter(
    prefix="/review",
    tags=["Pull Request Review"],
)


@router.post("/pr")
async def review_pull_request(request: Request):
    """
    Proxy Pull Request review requests to the Repository Service.
    """

    try:
        body = await request.json()
    except Exception:
        logger.warning("Invalid JSON payload for PR review request")
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid JSON payload"},
        )

    try:
        data, status = await ProxyClient.forward(
            method="POST",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/review/pr",
            headers={
                "authorization": request.headers.get("authorization", ""),
                "content-type": "application/json",
            },
            body=body,
            timeout=300.0,
        )

        return JSONResponse(
            status_code=status,
            content=data,
        )

    except Exception:
        logger.exception(
            "Unexpected error while proxying PR review request"
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal gateway error"},
        )
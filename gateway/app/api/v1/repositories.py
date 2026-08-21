import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.proxy import ProxyClient

logger = logging.getLogger("gateway.repositories")

router = APIRouter(tags=["Repositories"])


@router.get("/repositories")
async def list_repositories(request: Request):
    try:
        data, status = await ProxyClient.forward(
            method="GET",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/repositories",
            headers={
                key: value
                for key, value in request.headers.items()
                if key.lower() in {"authorization"}
            },
        )

        return JSONResponse(status_code=status, content=data)

    except Exception:
        logger.exception("Unexpected error while proxying repository list")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal gateway error"},
        )


@router.get("/repositories/{repo_id}")
async def repository_details(repo_id: int, request: Request):
    try:
        data, status = await ProxyClient.forward(
            method="GET",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/repositories/{repo_id}",
            headers={
                key: value
                for key, value in request.headers.items()
                if key.lower() in {"authorization"}
            },
        )

        return JSONResponse(status_code=status, content=data)

    except Exception:
        logger.exception(
            "Unexpected error while proxying repository details"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal gateway error"},
        )
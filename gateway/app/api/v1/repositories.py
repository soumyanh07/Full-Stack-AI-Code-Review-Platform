import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.dependencies.auth import get_current_user
from app.core.config import settings
from app.utils.proxy import ProxyClient


logger = logging.getLogger("gateway.repositories")

router = APIRouter(
    dependencies=[Depends(get_current_user)],
    tags=["Repositories"],
)


def _auth_headers(request: Request) -> dict:
    return {
        key: value
        for key, value in request.headers.items()
        if key.lower() == "authorization"
    }


@router.post("/repositories")
async def register_repository(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"detail": "Invalid JSON body"})

    try:
        data, status_code = await ProxyClient.forward(
            method="POST",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/repositories",
            headers=_auth_headers(request),
            body=body,
            timeout=15,
        )
        return JSONResponse(status_code=status_code, content=data)
    except Exception:
        logger.exception("Unexpected error while proxying repository registration")
        return JSONResponse(status_code=500, content={"detail": "Internal gateway error"})


@router.get("/repositories")
async def list_repositories(request: Request):
    try:
        data, status_code = await ProxyClient.forward(
            method="GET",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/repositories",
            headers=_auth_headers(request),
        )
        return JSONResponse(status_code=status_code, content=data)
    except Exception:
        logger.exception("Unexpected error while proxying repository list")
        return JSONResponse(status_code=500, content={"detail": "Internal gateway error"})


@router.get("/repositories/{repo_id}")
async def repository_details(repo_id: int, request: Request):
    try:
        data, status_code = await ProxyClient.forward(
            method="GET",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/repositories/{repo_id}",
            headers=_auth_headers(request),
        )
        return JSONResponse(status_code=status_code, content=data)
    except Exception:
        logger.exception("Unexpected error while proxying repository details")
        return JSONResponse(status_code=500, content={"detail": "Internal gateway error"})

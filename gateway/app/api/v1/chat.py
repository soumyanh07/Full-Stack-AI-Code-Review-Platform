import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.proxy import ProxyClient

logger = logging.getLogger("gateway.chat")

router = APIRouter(
    tags=["AI Chat"],
)


def _auth_headers(request: Request) -> dict:
    return {
        key: value
        for key, value in request.headers.items()
        if key.lower() == "authorization"
    }


@router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        data, status = await ProxyClient.forward(
            method="POST",
            url=f"{settings.REPOSITORY_SERVICE}/api/v1/chat",
            headers={
                **_auth_headers(request),
                "Content-Type": "application/json",
            },
            body=body,
            timeout=120.0,

        )

        return JSONResponse(
            status_code=status,
            content=data,
        )

    except Exception:
        logger.exception(
            "Unexpected error while proxying chat request"
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal gateway error"},
        )